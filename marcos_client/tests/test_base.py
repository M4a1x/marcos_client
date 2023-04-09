#!/usr/bin/env python3
#
# Base definitions and functions used for marga testing/simulation

import os
import pdb
import socket
import subprocess
import sys
import time
import unittest
import warnings
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import marcos_client.experiment as exp
import marcos_client.marcompile as mc
import marcos_client.server_comms as sc
from marcos_client.local_config import config

ip_address = "localhost"
port = 11111

# simulation configuration
marga_sim_path = Path(config["simulator"]["path"])
marga_sim_csv = Path(config["simulator"]["csv"])

marga_sim_fst_dump = config["simulator"]["fst_dump"]
marga_sim_fst = Path(config["simulator"]["fst"])

marga_sim_mem_file = Path(config["simulator"]["mem_file"])

# Arguments for compare_csv when running gradient tests
fhd_config = {
    "initial_bufs": np.array(
        [
            # see marga.sv, gradient control lines (lines 186-190, 05.02.2021)
            # strobe for both LSB and LSB, reset_n = 1, spi div = 10, grad board select (1 = ocra1, 2 = gpa-fhdo)
            (1 << 9) | (1 << 8) | (10 << 2) | 2,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        ],
        dtype=np.uint16,
    ),
    "latencies": np.array(
        [
            0,
            276,
            276,  # grad latencies match SPI div
            0,
            0,  # rx
            0,
            0,
            0,
            0,  # tx
            0,
            0,
            0,
            0,
            0,
            0,  # lo phase
            0,
            0,  # gates and LEDs, RX config
        ],
        dtype=np.uint16,
    ),
}

oc1_config = {
    "initial_bufs": np.array(
        [
            # see marga.sv, gradient control lines (lines 186-190, 05.02.2021)
            # strobe for both LSB and LSB, reset_n = 1, spi div = 10, grad board select (1 = ocra1, 2 = gpa-fhdo)
            (1 << 9) | (1 << 8) | (10 << 2) | 1,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        ],
        dtype=np.uint16,
    ),
    "latencies": np.array(
        [
            0,
            268,
            268,  # grad latencies match SPI div
            0,
            0,  # rx
            0,
            0,
            0,
            0,  # tx
            0,
            0,
            0,
            0,
            0,
            0,  # lo phase
            0,
            0,  # gates and LEDs, RX config
        ],
        dtype=np.uint16,
    ),
}

gb_orig = None
gb_changed = False


def set_grad_board(gb):
    global gb_orig, gb_changed
    if not gb_changed:
        gb_orig = mc.grad_board
    mc.grad_board = gb
    exp.grad_board = gb
    gb_changed = True


def restore_grad_board():
    global gb_orig, gb_changed
    mc.grad_board = gb_orig
    exp.grad_board = gb_orig
    gb_changed = False


def compare_csv(
    fname,
    sock,
    proc,
    initial_bufs=np.zeros(mc.MARGA_BUFS, dtype=np.uint16),
    latencies=np.zeros(mc.MARGA_BUFS, dtype=np.uint32),
    self_ref=True,  # use the CSV source file as the reference file to compare the output with
):
    source_csv = (Path(__file__).parent / "csvs" / fname).with_suffix(".csv").resolve()
    lc = mc.csv2bin(
        source_csv, quick_start=False, initial_bufs=initial_bufs, latencies=latencies
    )
    data = np.array(lc, dtype=np.uint32)

    # run simulation
    rx_data, msgs = sc.command({"run_seq": data.tobytes()}, sock)

    # halt simulation
    sc.send_packet(sc.construct_packet({}, 0, command=sc.close_server_pkt), sock)
    sock.close()
    proc.wait(1)  # wait a short time for simulator to close

    # compare resultant CSV with the reference
    if self_ref:
        rdata = np.loadtxt(source_csv, skiprows=1, delimiter=",", comments="#").astype(
            np.uint32
        )
        sdata = np.loadtxt(
            marga_sim_csv, skiprows=1, delimiter=",", comments="#"
        ).astype(np.uint32)

        rdata[1:, 0] -= rdata[1, 0]  # subtract off initial offset time
        sdata[1:, 0] -= sdata[1, 0]  # subtract off initial offset time

        return rdata.tolist(), sdata.tolist()
    else:
        ref_csv = (Path(__file__).parent / "csvs" / f"ref_{fname}.csv").resolve()
        with ref_csv.open() as ref:
            refl = ref.read().splitlines()
        with marga_sim_csv.open() as sim:
            siml = sim.read().splitlines()
        return refl, siml


def compare_dict(
    source_dict,
    ref_fname,
    sock,
    proc,
    initial_bufs=np.zeros(mc.MARGA_BUFS, dtype=np.uint16),
    latencies=np.zeros(mc.MARGA_BUFS, dtype=np.uint32),
    ignore_start_delay=True,
):
    lc = mc.dict2bin(source_dict, initial_bufs=initial_bufs, latencies=latencies)
    data = np.array(lc, dtype=np.uint32)

    # run simulation
    rx_data, msgs = sc.command({"run_seq": data.tobytes()}, sock)

    # halt simulation
    sc.send_packet(sc.construct_packet({}, 0, command=sc.close_server_pkt), sock)
    sock.close()
    proc.wait(1)  # wait a short time for simulator to close

    ref_csv = (Path(__file__).parent / "csvs" / ref_fname).with_suffix(".csv").resolve()
    with ref_csv.open() as ref:
        refl = ref.read().splitlines()
    with marga_sim_csv.open() as sim:
        siml = sim.read().splitlines()
    # return refl, siml

    ref_csv = (Path(__file__).parent / "csvs" / ref_fname).with_suffix(".csv").resolve()
    if ignore_start_delay:
        rdata = np.loadtxt(ref_csv, skiprows=1, delimiter=",", comments="#").astype(
            np.uint32
        )
        sdata = np.loadtxt(
            marga_sim_csv, skiprows=1, delimiter=",", comments="#"
        ).astype(np.uint32)

        rdata[1:, 0] -= rdata[1, 0]  # subtract off initial offset time
        sdata[1:, 0] -= sdata[1, 0]  # subtract off initial offset time

        return rdata.tolist(), sdata.tolist()
    else:
        with ref_csv.open() as ref:
            refl = ref.read().splitlines()
        with marga_sim_csv.open() as sim:
            siml = sim.read().splitlines()
        return refl, siml


def expt_run(e):
    """Function for customising how compare_expt_dict() runs Experiments; e.g. for testing different Experiment methods etc
    (see test_lo_change_expt in test_marga_model.py for an example)"""
    rx_data, msgs = e.run()
    return rx_data, msgs


def compare_expt_dict(
    source_dict,
    ref_fname,
    sock,
    proc,
    # initial_bufs=np.zeros(mc.MARGA_BUFS, dtype=np.uint16),
    # latencies=np.zeros(mc.MARGA_BUFS, dtype=np.uint32),
    ignore_start_delay=True,
    run_fn=expt_run,
    **kwargs,
):
    """Arguments the same as for compare_dict(), except that the source
    dictionary is in floating-point units, and the kwargs are passed
    to the Experiment class constructor. Note that the initial_bufs
    and latencies are supplied to the Experiment class from the
    classes in grad_board.py.
    """

    e = exp.Experiment(prev_socket=sock, seq_dict=source_dict, **kwargs)

    # run simulation
    rx_data, msgs = run_fn(e)

    # halt simulation
    sc.send_packet(sc.construct_packet({}, 0, command=sc.close_server_pkt), sock)
    sock.close()
    proc.wait(1)  # wait a short time for simulator to close

    ref_csv = (Path(__file__).parent / "csvs" / ref_fname).with_suffix(".csv").resolve()
    with ref_csv.open() as ref:
        refl = ref.read().splitlines()
    with marga_sim_csv.open() as sim:
        siml = sim.read().splitlines()
    # return refl, siml

    ref_csv = (Path(__file__).parent / "csvs" / ref_fname).with_suffix(".csv").resolve()
    if ignore_start_delay:
        rdata = np.loadtxt(ref_csv, skiprows=1, delimiter=",", comments="#").astype(
            np.uint32
        )
        sdata = np.loadtxt(
            marga_sim_csv, skiprows=1, delimiter=",", comments="#"
        ).astype(np.uint32)

        rdata[1:, 0] -= rdata[1, 0]  # subtract off initial offset time
        sdata[1:, 0] -= sdata[1, 0]  # subtract off initial offset time

        return rdata.tolist(), sdata.tolist()
    else:
        with ref_csv.open() as ref:
            refl = ref.read().splitlines()
        with marga_sim_csv.open() as sim:
            siml = sim.read().splitlines()
        return refl, siml
