# control.py

from device_manager import DeviceManager

# THIS PATH WILL ONLY WORK ON THE LAB PC
VOA_DEVICE_PATH = "/dev/serial/by-id/PUT_REAL_PATH_HERE"

def main():
    dm = DeviceManager()

    print("Connecting to VOA...")
    dm.connect_voa(VOA_DEVICE_PATH)

    while True:
        print("\nOptions:")
        print("1) Set attenuation")
        print("2) Read attenuation")
        print("3) Exit")

        choice = input("Select option: ")

        if choice == "1":
            value = float(input("Enter attenuation (dB): "))
            dm.set_voa_attenuation(value)
            print("Attenuation set.")

        elif choice == "2":
            att = dm.get_voa_attenuation()
            print("Current attenuation:", att, "dB")

        elif choice == "3":
            print("Exiting...")
            dm.close_all()
            break

        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
