from base import LocalGateway, base_logger


app = LocalGateway()


async def other():
    base_logger.info("HELLO WORLD!!! You did it! :D")
    return


async def test():
    """
    Test example of dynamically deploying another route upon an HTTP request

    Since this function will be invoked once the `test` event is triggered,
    the route `/api/other` will be registered at runtime rather than upon 
    starting the server. Such behavior allows to dynamically create functions
    that could answer to new events. Be aware that registering two functions
    with the same name will result in only one route. You can change this
    behavior by providing the `path` argument.

    Once this new route is registered, you will see it in the Homecare Hub under
    SIF Status, which means upon receiving an event (in this case `test`), you
    will see in the logs of this example the print above.
    """
    app.deploy(other, "testing-2", "test", path="testing")
    return {"status": 200}

# Deploy a route within this server to be reachable from the SIF scheduler
# it appends the name of the cb to `/api/`. For more, please read the
# documentation for `deploy`
app.deploy(test, "testing", "test")