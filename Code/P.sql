create database P;
use P ;

#Doctors Table : Doctors will be capable work with data of patients and see the drugs and choose it 
create table doctor (
Doctor_ID INT primary key ,
Doctor_Name VARCHAR(50) ,
Doctor_Department VARCHAR(50) 
);
INSERT INTO doctor (Doctor_ID, Doctor_Name, Doctor_Department) VALUES
(5511, 'Dr. Shaker Elsappagh', 'Cardiology'),
(5522, 'Dr. Radwa Hassan', 'General Surgery');
select * from orders;
#Patients that will be all process depend on there medical data and prescreption done on themm
create table patient (
Patient_ID INT primary key  ,
Patient_Age INT ,
Patient_Gender VARCHAR(50) ,
Patient_Name VARCHAR(50) ,
Patient_Medication TEXT ,
Patient_Diagnoses TEXT 
);
INSERT INTO patient (Patient_ID, Patient_Name,Patient_Age,Patient_Gender, Patient_Medication, Patient_Diagnoses) VALUES
(511, 'Alice Brown',45,'Female','Data about Alice', 'Hypertension'),
(512, 'Bob Knight',55,'Male', 'Data about Bob', 'Diabetes'),
(513, 'Charlie Johnson',65,'Male', 'Data about Charlie', 'Asthma'),
(514, 'Diane Evans', 55,'Male','Data about Diane', 'Thyroid Disorder'),
(515, 'Edward Collins',71,'Male', 'Data about Edward', 'Arthritis');
#There responsiblity to take orders and managing inventory 
CREATE TABLE pharmacist (
    Pharmacist_ID INT PRIMARY KEY,
    Pharmacist_Name VARCHAR(50)
);
INSERT INTO pharmacist (Pharmacist_ID, Pharmacist_Name) VALUES
(9911, 'Pharm John Doe'),
(9922, 'Pharm Jane Smith'),
(9933, 'Pharm Emily Stone'),
(9944, 'Pharm Mike Brown');

# Drug and Active Ingredients data 
CREATE TABLE IF NOT EXISTS drugs (
    Drug_ID INT AUTO_INCREMENT PRIMARY KEY,
    Drug_Name VARCHAR(255) NOT NULL,
    Quantity INT NOT NULL,
    Dose VARCHAR(255) NOT NULL,
    Expiration_date DATE NOT NULL,
    Manufacturer VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS active_ingredients (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Drug_ID INT,
    Active_ingredient VARCHAR(255) NOT NULL,
    FOREIGN KEY (Drug_ID) REFERENCES drugs(Drug_ID)
);
INSERT INTO drugs (Drug_ID, Drug_Name, Quantity, Dose, Expiration_date, Manufacturer) VALUES
(723, 'Amoxicillin', 100, '10 mg', '2024-06-27', 'Manufacturer A'),
(855332, 'Ciprofloxacin', 100, '10 mg', '2024-06-27', 'Manufacturer B'),
(115170, 'Azithromycin', 100, '10 mg', '2024-06-27', 'Manufacturer C'),
(212121, 'Sertraline', 100, '10 mg', '2024-06-27', 'Manufacturer D'),
(21227, 'Fluoxetine', 100, '10 mg', '2024-06-27', 'Manufacturer E'),
(204299, 'Citalopram', 100, '10 mg', '2024-06-27', 'Manufacturer F'),
(5640, 'Ibuprofen', 100, '10 mg', '2024-06-27', 'Manufacturer G'),
(161, 'Acetaminophen', 100, '10 mg', '2024-06-27', 'Manufacturer H'),
(1191, 'Aspirin', 100, '10 mg', '2024-06-27', 'Manufacturer I'),
(29046, 'Lisinopril', 100, '10 mg', '2024-06-27', 'Manufacturer J'),
(197361, 'Amlodipine', 100, '10 mg', '2024-06-27', 'Manufacturer K'),
(897122, 'Losartan', 100, '10 mg', '2024-06-27', 'Manufacturer L'),
(86009, 'Metformin', 100, '10 mg', '2024-06-27', 'Manufacturer M'),
(197935, 'Glibenclamide', 100, '10 mg', '2024-06-27', 'Manufacturer N'),
(897097, 'Pioglitazone', 100, '10 mg', '2024-06-27', 'Manufacturer O');

# If Each Drug have more than one active ingredients
INSERT INTO active_ingredients (Drug_ID, Active_ingredient) VALUES
(723, 'Amoxicillin Active Ingredient'),
(855332, 'Ciprofloxacin Active Ingredient'),
(115170, 'Azithromycin Active Ingredient'),
(212121, 'Sertraline Active Ingredient'),
(21227, 'Fluoxetine Active Ingredient'),
(204299, 'Citalopram Active Ingredient'),
(5640, 'Ibuprofen Active Ingredient'),
(161, 'Acetaminophen Active Ingredient'),
(1191, 'Aspirin Active Ingredient'),
(29046, 'Lisinopril Active Ingredient'),
(197361, 'Amlodipine Active Ingredient'),
(897122, 'Losartan Active Ingredient'),
(86009, 'Metformin Active Ingredient'),
(197935, 'Glibenclamide Active Ingredient'),
(897097, 'Pioglitazone Active Ingredient');
#Drugs Data that have conflict 
CREATE TABLE drug_conflict (
    Drug_Conflict_ID INT PRIMARY KEY,
    Drug_Conflict_Name VARCHAR(50)
);
INSERT INTO drug_conflict (Drug_Conflict_ID, Drug_Conflict_Name) VALUES 
(5640, 'Ibuprofen'),
(1191, 'Aspirin'),
(855332, 'Ciprofloxacin');
#Relation that check the interaction (conflict between drugs)
CREATE TABLE drug_drug_conflict (
    Drug_ID INT,
    Drug_Conflict_ID INT,
    PRIMARY KEY (Drug_ID, Drug_Conflict_ID),
    FOREIGN KEY (Drug_ID) REFERENCES drugs(Drug_ID),
    FOREIGN KEY (Drug_Conflict_ID) REFERENCES drug_conflict(Drug_Conflict_ID)
);
INSERT INTO drug_drug_conflict (Drug_ID, Drug_Conflict_ID) VALUES
(855332, 5640),
(21227, 5640),
(212121, 1191),
(29046, 1191),
(86009, 855332),
(21227, 855332);
#Table contain the bought drugs grom pharmacy by the doctor and being sent to the pharmacist 
CREATE TABLE orders (
	Patient_ID INT,
    Doctor_ID INT,
    Order_ID INT AUTO_INCREMENT PRIMARY KEY,
    Drug_ID INT,
    Quantity INT,
    Drug_Name VARCHAR(50),
    Dose VARCHAR(50),
    FOREIGN KEY (Drug_ID) REFERENCES drugs(Drug_ID),
    FOREIGN KEY (Patient_ID) references patient(Patient_ID),
    FOREIGN KEY (Doctor_ID) references doctor(Doctor_ID)
);
#Diagnosis table with ICD-10 
create table diagnosis (
 diagnosis_id varchar(5) primary key ,
 diagnosis_content varchar(50)
 );
INSERT INTO diagnosis(diagnosis_id, diagnosis_content) VALUES ('I10', 'Hypertension (High Blood Pressure)');
INSERT INTO diagnosis(diagnosis_id, diagnosis_content) VALUES ('I25.10', 'Coronary Artery Disease');
INSERT INTO diagnosis(diagnosis_id, diagnosis_content) VALUES ('I50.9', 'Heart Failure');
INSERT INTO diagnosis(diagnosis_id, diagnosis_content) VALUES ('I48.91', 'Atrial Fibrillation');
INSERT INTO diagnosis(diagnosis_id, diagnosis_content) VALUES ('I21.9', 'Myocardial Infarction (Heart Attack)');
INSERT INTO diagnosis(diagnosis_id, diagnosis_content) VALUES ('I42.9', 'Cardiomyopathy');
INSERT INTO diagnosis(diagnosis_id, diagnosis_content) VALUES ('I35.0', 'Aortic Valve Stenosis');
INSERT INTO diagnosis(diagnosis_id, diagnosis_content) VALUES ('I73.9', 'Peripheral Artery Disease');
INSERT INTO diagnosis(diagnosis_id, diagnosis_content) VALUES ('I26.9', 'Pulmonary Embolism');
INSERT INTO diagnosis(diagnosis_id, diagnosis_content) VALUES ('I33.0', 'Endocarditis');
#Relation to help us address if there is a conflict between patient diagnosis and the selected drugs
 create table diagnosis_drug_conflict (
 diagnosis_id varchar(5)  ,
 Drug_ID int ,
 primary key(diagnosis_id,Drug_ID) ,
 foreign key (diagnosis_id) references diagnosis(diagnosis_id),
 foreign key (Drug_ID) references drugs(Drug_ID)
  );
INSERT INTO diagnosis_drug_conflict (diagnosis_id, Drug_ID) VALUES 
('I50.9', 1191),
('I10', 5640);
#Table for alternntives to choose from if there are any conflicts
CREATE TABLE drug_alternatives (
    Drug_ID INT,
    Drug_Name VARCHAR(50),
    Alternative_Drug_ID INT,
    Alternative_Drug_Name VARCHAR(50),
    PRIMARY KEY (Drug_ID, Alternative_Drug_ID)
);
 
