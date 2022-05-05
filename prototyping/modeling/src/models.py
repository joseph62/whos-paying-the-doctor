from dataclasses import dataclass

@dataclass
class ChungusGeneralPayment:
    record_id: int
    change_type: str
    covered_recipient_type: str
    teaching_hospital_ccn: str
    teaching_hospital_id: str
    teaching_hospital_name: str
    physician_id: int
    physician_first_name: str
    physician_middle_name: str
    physician_last_name: str
    physician_name_suffix: str
    physician_primary_type: str
    physician_specialty: str
    physician_license_state_code_1: str
    physician_license_state_code_2: str
    physician_license_state_code_3: str
    physician_license_state_code_4: str
    physician_license_state_code_5: str
    recipient_primary_business_street_address_line_1: str
    recipient_primary_business_street_address_line_2: str
    recipient_city: str
    recipient_state: str
    recipient_zip_code: str
    recipient_country: str
    recipient_province: str
    recipient_postal_code: str
    submitting_applicable_manufacturer_or_applicable_gpo_name: str
    applicable_manufacturer_or_applicable_gpo_making_payment_id: str
    applicable_manufacturer_or_applicable_gpo_making_payment_name: str
    applicable_manufacturer_or_applicable_gpo_making_payment_state: str
    applicable_manufacturer_or_applicable_gpo_making_payment_country: str
    total_amount_of_payment_us_dollars: float
    date_of_payment: str
    number_of_payments_included_in_total_amount: int
    form_of_payment_or_transfer_of_value: str
    nature_of_payment_or_transfer_of_value: str
    city_of_travel: str
    state_of_travel: str
    country_of_travel: str
    physician_ownership_indicator: str
    third_party_payment_recipient_indicator: str
    name_of_third_party_entity_receiving_payment_or_transfer_of_value: str
    charity_indicator: str
    third_party_equals_covered_recipient_indicator: str
    contextual_information: str
    delay_in_publication_indicator: str
    dispute_status_for_publication: str
    product_indicator: str
    name_of_associated_covered_drugs_or_biologicals1: str
    name_of_associated_covered_drugs_or_biologicals2: str
    name_of_associated_covered_drugs_or_biologicals3: str
    name_of_associated_covered_drugs_or_biologicals4: str
    name_of_associated_covered_drugs_or_biologicals5: str
    ndc_of_associated_covered_drugs_or_biologicals1: str
    ndc_of_associated_covered_drugs_or_biologicals2: str
    ndc_of_associated_covered_drugs_or_biologicals3: str
    ndc_of_associated_covered_drugs_or_biologicals4: str
    ndc_of_associated_covered_drugs_or_biologicals5: str
    name_of_associated_covered_device_or_medical_supply1: str
    name_of_associated_covered_device_or_medical_supply2: str
    name_of_associated_covered_device_or_medical_supply3: str
    name_of_associated_covered_device_or_medical_supply4: str
    name_of_associated_covered_device_or_medical_supply5: str
    program_year: str
    payment_publication_date: str

@dataclass
class GeneralPayment:
    record_id: int
    change_type: str
    covered_recipient_type: str
    teaching_hospital: "TeachingHospital"
    physician: "Physician"
    submitting_applicable_manufacturer_or_gpo_making_payment: "ManufacturerOrGPO"
    total_amount_of_payment_us_dollars: float
    date_of_payment: str
    number_of_payments_included_in_total_amount: int
    form_of_payment_or_transfer_of_value: str
    nature_of_payment_or_transfer_of_value: str
    city_of_travel: str
    state_of_travel: str
    country_of_travel: str
    physician_ownership_indicator: str
    third_party_payment_recipient_indicator: str
    name_of_third_party_entity_receiving_payment_or_transfer_of_value: str
    charity_indicator: str
    third_party_equals_covered_recipient_indicator: str
    contextual_information: str
    delay_in_publication_indicator: str
    dispute_status_for_publication: str
    product_indicator: str
    associated_covered_drugs_or_biologicals: "list[CoveredDrugOrBiological]"
    name_of_associated_covered_device_or_medical_supply1: str
    name_of_associated_covered_device_or_medical_supply2: str
    name_of_associated_covered_device_or_medical_supply3: str
    name_of_associated_covered_device_or_medical_supply4: str
    name_of_associated_covered_device_or_medical_supply5: str
    program_year: str
    payment_publication_date: str

@dataclass
class CoveredDrugOrBiological:
    ndc: str
    name: str

@dataclass
class ManufacturerOrGPO:
    id: str
    name: str
    state: str
    country: str

@dataclass
class Recipient:
    address_line_1: str
    address_line_2: str
    city: str
    state: str
    zip_code: str
    country: str
    province: str
    postal_code: str

@dataclass
class TeachingHospital(Recipient):
    id: int
    ccn: str
    name: str

@dataclass
class Physician(Recipient):
    profile_id: int
    first_name: str
    middle_name: str
    last_name: str
    name_suffix: str
    primary_type: str
    specialty: str
    state_codes: list[str]
