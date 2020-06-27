fhir = pdspi.pds_fhir_loader.get_entries(json_in_dir=json_in_dir, pids=pids, resource_names=resource_names)
for pid in pids:
    age_unit = "year"
    height_unit = "m"
    weight_unit = "kg"
    bmi_unit = "kg/m^2"
    resource_names = ["Patient", "Observation", "Condition", "MedicationRequest"]
    intervention = pdsphenotypemapping.clinical_feature.intervention(X=X, Y=Y, study_start=study_start, study_end=study_end, records=medication_request)
    age = pdsphenotypemapping.clinical_feature.age(unit=age_unit, timestamp=timestamp, patient=patient)
    bmi = pdsphenotypemapping.clinical_feature.bmi(height=height, weight=weight, unit=bmi_unit, timestamp=timestamp, records=observation)
    height = pdsphenotypemapping.clinical_feature.height(unit=height_unit, timestamp=timestamp, records=observation)
    weight = pdsphenotypemapping.clinical_feature.weight(unit=weight_unit, timestamp=timestamp, records=observation)
    patient = pdsphenotypemapping.clinical_feature.get_patient(patient_id=pid, fhir=fhir)
    medication_request = pdsphenotypemapping.clinical_feature.get_medication_request(patient_id=pid, fhir=fhir)
    condition = pdsphenotypemapping.clinical_feature.get_condition(patient_id=pid, fhir=fhir)
    observation = pdsphenotypemapping.clinical_feature.get_observation(patient_id=pid, fhir=fhir)
    return {
      "age" : age,
      "bmi" : bmi,
      "height": height,
      "weight": weight
    }
