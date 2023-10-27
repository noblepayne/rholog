import logging
import time
import uuid

import rholog as ρ


def step1(log):
    with ρ.trace(log, "step1") as log:
        time.sleep(1)


def step2_substep1(log):
    with ρ.trace(log, "step2_substep1") as log:
        time.sleep(1)


def step2_substep2(log):
    with ρ.trace(log, "step2_substep2") as log:
        log.info("long sleep time")
        time.sleep(4)
        log.info("done sleeping")


def step2(log):
    with ρ.trace(log, "step2") as log:
        step2_substep1(log)
        time.sleep(1)
        step2_substep2(log)


def main(log, root_id):
    with ρ.trace(log, "main", root_id=root_id) as log:
        step1(log)
        step2(log)


if __name__ == "__main__":
    root_id = uuid.uuid4().hex
    ρ.setup_logging(indent=2)
    log = logging.getLogger("demo1")
    main(log, root_id)
