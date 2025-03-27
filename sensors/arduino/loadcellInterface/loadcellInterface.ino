// #include <SD.h> // Include the SD library

int analogPin=A0;
float val =0.0;
float Vmax=5;
float sensorRange=1;
float conversion = Vmax*sensorRange/1023.0;
unsigned long StartTime = 0;
unsigned long CurrentTime=0;

// File dataFile; // File object to store data

void setup() {
  // put your setup code here, to run once:
Serial.begin(9600); // Initialize serial communication at 9600 baud
// if (!SD.begin(10)) {
//     Serial.println("SD card initialization failed!");
//     return;
//   }

//   // Create or open the data file
//   dataFile = SD.open("data.csv", FILE_WRITE);
//   if (!dataFile) {
//     Serial.println("Error opening data.csv!");
//     return;
//   }

  // Write headers to the CSV file
  Serial.println("Force, Time");
  // dataFile.flush();
 StartTime = millis();
// Serial.println("Device setup");
}

void loop() {
  // put your main code here, to run repeatedly:
  val=conversion*analogRead(analogPin);
  // Serial.print("Val:");
  Serial.print(val);
  Serial.print(",");
  CurrentTime = millis();  
  // dataFile.print(val);
  // dataFile.print(", ");
  // dataFile.println( CurrentTime - StartTime);
  // dataFile.flush();
  Serial.println(CurrentTime - StartTime);
}
