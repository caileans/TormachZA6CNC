import serial
import csv

# download the serial package using 'pip install pyserial'

ser = serial.Serial('COM5', 9600)  # Adjust COM port as needed
with open('data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    while True:
        line = ser.readline().decode('utf-8').strip()
        writer.writerow([line])