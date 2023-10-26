import asyncio, json
import aiohttp
from controller import network_manager
from controller.utils import PubSub
import docker


async def log_collector(nm: network_manager.NetworkManager, pubsub: PubSub):
    client = docker.client.from_env()
    while True:
        for qnode in nm.qnodes:
            log = qnode.get_log(client)
            if log:
                pubsub.publish(
                    json.dumps(
                        {
                            "qnode_id": qnode.id,
                            "type": "log",
                            "data": log.decode("utf-8"),
                        }
                    )
                )
        await asyncio.sleep(0.5)


async def qnode_status_collector(nm: network_manager.NetworkManager, pubsub: PubSub):
    while True:
        for qnode in nm.qnodes:
            url = f"http://{qnode.ip}:8080/status"
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url, headers={"Content-Type": "application/json"}
                ) as response:
                    resp = await response.json()
                    resp["qnode_id"] = qnode.id
                    resp["type"] = "qnode_status"
                    pubsub.publish(json.dumps(resp))
        await asyncio.sleep(5)


async def network_collector(nm: network_manager.NetworkManager, pubsub: PubSub):
    while True:
        nm.fetch_network_info()
        network = nm.get_network()
        obj = network.model_dump(mode="json")
        obj["type"] = "network"
        pubsub.publish(json.dumps(obj))
        await asyncio.sleep(5)
