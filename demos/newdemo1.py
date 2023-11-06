import logging
import time

import rholog.jsonformatter
import rholog.jsonlog_span_publisher
import rholog.p as p


def main():
    rholog.jsonformatter.log_json_to_stdout(indent=2)
    log = logging.getLogger("demo")
    publisher = rholog.jsonlog_span_publisher.publisher(log)
    tracer = p.tracer(publisher)
    with tracer("junk") as span:
        time.sleep(1)
        with span("more_junk") as span:
            time.sleep(1)
            span.update(
                context={"updated_context": "i_hope"}, tags={"updated_tags": "lets_see"}
            )
            with span("even_more_junk") as span:
                span.event("about to sleep!")
                time.sleep(1)
                span.event("finished sleeping")
                1 / 0


if __name__ == "__main__":
    main()
