import logging
import time
import uuid

import rholog as ρ


def step1():
    time.sleep(1)


def step2_substep1():
    time.sleep(1)


def step2_substep2(log):
    ρ.event(log, "long sleep time")
    time.sleep(4)
    ρ.event(log, "done sleeping")
    1 / 0


def step2(log):
    step2_substep1()
    time.sleep(1)
    step2_substep2(log)


def main(log, root_id):
    with ρ.trace(log, "main", root_id=root_id) as log:
        step1()
        step2(log)


if __name__ == "__main__":
    root_id = uuid.uuid4().hex
    ρ.setup_logging()
    log = logging.getLogger("demo2")
    main(log, root_id)
