create database P;
use P ;
##########################################Entities##############################################################
#Doctors Data Doctors will be capable work with data of patients and see the drugs and choose it 
create table doctor (
Doctor_ID INT primary key ,
Doctor_Name VARCHAR(50) ,
Doctor_Department VARCHAR(50) 
);
INSERT INTO doctor (Doctor_ID, Doctor_Name, Doctor_Department) VALUES
(5511, 'Dr. Shaker Elsappagh', 'Cardiology'),
(5522, 'Dr. Radwa Hassan', 'General Surgery');
select * from orders;
#patients that will be all operations done on themm
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
#will be responsible for drug orders handling and manage inventory
CREATE TABLE pharmacist (
    Pharmacist_ID INT PRIMARY KEY,
    Pharmacist_Name VARCHAR(50)
);
INSERT INTO pharmacist (Pharmacist_ID, Pharmacist_Name) VALUES
(9911, 'Pharm John Doe'),
(9922, 'Pharm Jane Smith'),
(9933, 'Pharm Emily Stone'),
(9944, 'Pharm Mike Brown');
#Drugs table 
CREATE TABLE IF NOT EXISTS drugs (
    Drug_ID INT AUTO_INCREMENT PRIMARY KEY,
    Drug_Name VARCHAR(255) NOT NULL,
    Quantity INT NOT NULL,
    Dose VARCHAR(255) NOT NULL
);
INSERT INTO drugs (Drug_ID,Drug_Name, Quantity, Dose) VALUES (723,'Amoxicillin', 100, '10 mg');
INSERT INTO drugs (Drug_ID,Drug_Name, Quantity, Dose) VALUES (855332,'Ciprofloxacin', 100, '10 mg');
INSERT INTO drugs (Drug_ID,Drug_Name, Quantity, Dose) VALUES (115170,'Azithromycin', 100, '10 mg');
INSERT INTO drugs (Drug_ID,Drug_Name, Quantity, Dose) VALUES (212121,'Sertraline', 100, '10 mg');
INSERT INTO drugs (Drug_ID,Drug_Name, Quantity, Dose) VALUES (21227,'Fluoxetine', 100, '10 mg');
INSERT INTO drugs (Drug_ID,Drug_Name, Quantity, Dose) VALUES (204299,'Citalopram', 100, '10 mg');
INSERT INTO drugs (Drug_ID,Drug_Name, Quantity, Dose) VALUES (5640,'Ibuprofen', 100, '10 mg');
INSERT INTO drugs (Drug_ID,Drug_Name, Quantity, Dose) VALUES (161,'Acetaminophen', 100, '10 mg');
INSERT INTO drugs (Drug_ID,Drug_Name, Quantity, Dose) VALUES (1191,'Aspirin', 100, '10 mg');
INSERT INTO drugs (Drug_ID,Drug_Name, Quantity, Dose) VALUES (29046,'Lisinopril', 100, '10 mg');
INSERT INTO drugs (Drug_ID,Drug_Name, Quantity, Dose) VALUES (197361,'Amlodipine', 100, '10 mg');
INSERT INTO drugs (Drug_ID,Drug_Name, Quantity, Dose) VALUES (897122,'Losartan', 100, '10 mg');
INSERT INTO drugs (Drug_ID,Drug_Name, Quantity, Dose) VALUES (86009,'Metformin', 100, '10 mg');
INSERT INTO drugs (Drug_ID,Drug_Name, Quantity, Dose) VALUES (197935,'Glibenclamide', 100, '10 mg');
INSERT INTO drugs (Drug_ID,Drug_Name, Quantity, Dose) VALUES (897097,'Pioglitazone', 100, '10 mg');
#Drugs that may make conflict with each other
CREATE TABLE drug_conflict (
    Drug_Conflict_ID INT PRIMARY KEY,
    Drug_Conflict_Name VARCHAR(50)
);
INSERT INTO drug_conflict (Drug_Conflict_ID, Drug_Conflict_Name) VALUES (5640, 'Ibuprofen');
INSERT INTO drug_conflict (Drug_Conflict_ID, Drug_Conflict_Name) VALUES (1191, 'Aspirin');
INSERT INTO drug_conflict (Drug_Conflict_ID, Drug_Conflict_Name) VALUES (855332, 'Ciprofloxacin');
#relation that map each conflict with the drug
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
(21227,855332);
#orders that eill made by doctor and sent to the pharmacist 

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

 create table diagnosis_drug_conflict (
 diagnosis_id varchar(5)  ,
 Drug_ID int ,
 primary key(diagnosis_id,Drug_ID) ,
 foreign key (diagnosis_id) references diagnosis(diagnosis_id),
 foreign key (Drug_ID) references drugs(Drug_ID)
  );
INSERT INTO diagnosis_drug_conflict(diagnosis_id,Drug_ID ) VALUES ('I50.9',1191);
INSERT INTO diagnosis_drug_conflict(diagnosis_id,Drug_ID ) VALUES ('I10', 5640);
 
 