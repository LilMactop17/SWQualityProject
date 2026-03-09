import asyncio
import zenoh
from kuksa_client.grpc.aio import VSSClient

async def main():
    print("Connecting to Zenoh...")
    conf = zenoh.Config()
    conf.insert_json5("connect/endpoints", '["tcp/127.0.0.1:7447"]')
    z_session = zenoh.open(conf)

    print("Connecting to Kuksa Databroker...")
    async with VSSClient('127.0.0.1', 55555) as kuksa_client:
        while True:
            updates = await kuksa_client.get_current_values([
                'Vehicle.OBD.VehicleSpeed',
                'Vehicle.OBD.EngineSpeed',
                'Vehicle.OBD.ThrottlePosition',
                'Vehicle.OBD.CoolantTemperature',
            ])

            for path, data_point in updates.items(): #path is the VSS string, data_point is the value for the string
                if data_point is not None:
                    zenoh_key = path.replace(".", "/")
                    z_session.put(zenoh_key, str(data_point.value))
                    print(f"Zenoh Pub -> {zenoh_key}: {data_point.value}")

            await asyncio.sleep(1)

asyncio.run(main())
