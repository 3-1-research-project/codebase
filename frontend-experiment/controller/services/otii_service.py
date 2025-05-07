import csv
import datetime
import json
from otii_tcp_client import otii_connection, otii as otii_application
from otii_tcp_client import arc as otii_arc


class OtiiService:
    otii_app: any

    def __init__(self, host: str = "127.0.0.1", port: int = 1905):
        connection = otii_connection.OtiiConnection("127.0.0.1", 1905)
        connect_response = connection.connect_to_server(try_for_seconds=10)
        if connect_response["type"] == "error":
            raise Exception(
                f'Exit! Error code: {connect_response["errorcode"]}, '
                f'Description: {connect_response["payload"]["message"]}'
            )
        self.otii_app = otii_application.Otii(connection)

    def configure_multimeter(self) -> tuple[any, any]:
        # Based on the example from
        # https://github.com/qoitech/otii-tcp-client-python/blob/master/examples/basic_measurement.py
        devices = self.otii_app.get_devices()
        if len(devices) == 0:
            raise Exception("No Arc or Ace connected!")
        device = devices[0]

        # Enable the main current, voltage, and power channels

        # device.enable_channel(Channel.MAIN_CURRENT)
        # device.enable_channel(Channel.MAIN_VOLTAGE)
        # device.enable_channel(Channel.MAIN_POWER)

        # device.set_channel_samplerate(Channel.MAIN_CURRENT, 10000)
        # device.set_channel_samplerate(Channel.MAIN_VOLTAGE, 10000)
        # device.set_channel_samplerate(Channel.MAIN_POWER, 10000)

        device.enable_channel("mc", True)
        device.enable_channel("mv", True)
        device.enable_channel("mp", True)

        device.set_channel_samplerate("mc", 10000)
        device.set_channel_samplerate("mv", 10000)
        device.set_channel_samplerate("mp", 10000)

        # Get the active project
        project = self.otii_app.get_active_project()

        return project, device

    def collect_data(
        self,
        otii_project: otii_application.project.Project,
        device: otii_arc.Arc,
        schema_path: str,
        iteration: int,
    ):
        # Get statistics for the recording

        recording = otii_project.get_last_recording()
        # info = recording.get_channel_info(device.id, "mc")
        # statistics = recording.get_channel_statistics(
        #     device.id, "mc", info["from"], info["to"]
        # )

        current_count = recording.get_channel_data_count(device.id, "mc")
        voltage_count = recording.get_channel_data_count(device.id, "mv")
        power_count = recording.get_channel_data_count(device.id, "mp")

        # Create a CSV file
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        schema = schema_path.split("/")[-1].split(".")[0]
        filename = f"{schema}_{iteration}_{timestamp}.csv"

        with open(filename, mode="w") as data_file:
            # Header
            data_writer = csv.writer(
                data_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            data_writer.writerow(["seconds", "current", "voltage", "power"])

            # Write data
            print("Writing data to CSV...")

            index = 0
            while index < current_count:
                current_data = recording.get_channel_data(device.id, "mc", index, 1000)[
                    "values"
                ]
                voltage_data = recording.get_channel_data(device.id, "mv", index, 1000)[
                    "values"
                ]
                power_data = recording.get_channel_data(device.id, "mp", index, 1000)[
                    "values"
                ]

                # add to csv
                for i in range(len(current_data)):
                    data_writer.writerow(
                        [
                            (index + i) / 10000,
                            current_data[i],
                            voltage_data[i],
                            power_data[i],
                        ]
                    )

                index += len(current_data)

        print(f"Data saved to {filename}!")