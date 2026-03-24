# ==============================================================================
# UPS Credentials and Configuration
# ==============================================================================
UPS_CARRIER_NAME = "UPS"
UPS_CLIENT_ID = "7WSnxKncCMa5mhBZIPwMv5zxnhXRsNTIt5z6IwsicieNrdG2"
UPS_CLIENT_SECRET = "uENQxqH6pWWhxUTIf8iQy8jJlLXBxTaJhRZ9qiGP7VPoqB0qAYgI8ctPtpeEzw53"
UPS_TOKEN_URL = "https://wwwcie.ups.com/security/v1/oauth/token"
UPS_DEV_BASE_URL = "https://wwwcie.ups.com/api"
UPS_PROD_BASE_URL = "https://onlinetools.ups.com/api"
UPS_SHIPPER_NUMBER = "RC6604"

UPS_API_VERSION_RATING = "v2409"
UPS_API_VERSION_SHIPMENT = "v2409"
UPS_API_VERSION_TRACKING = "v1"
UPS_API_VERSION_ADDRESS_VALIDATION = "v3"

UPS_REQUEST_OPTION_RATING = "Shoptimeintransit"
UPS_REQUEST_OPTION_ADDRESS_VALIDATION = "3"
UPS_REQUEST_OPTION_SHIPMENT_SUBVERSION = "1801"
UPS_REQUEST_OPTION_SHIPMENT_REQUEST_OPTION = "nonvalidate"

UPS_SHIPPER_NAME = "Thisai"
UPS_SHIPPER_CITY = "SIMI VALLEY"
UPS_SHIPPER_POSTAL_CODE = "93063"
UPS_SHIPPER_COUNTRY_CODE = "US"
UPS_SHIPPER_ADDRESS_LINE1 = "1834 Blazewood Street"
UPS_SHIPPER_STATE_PROVINCE_CODE = "CA"
UPS_SHIPPER_CHARGE_TYPE = "01"  # Transportation charge

UPS_TRANSACTION_ID = "thisai-transaction"
UPS_TRANSACTION_SRC = "ThisaiApp"
UPS_CUSTOMER_CONTEXT = "Thisai Booking"

# UPS API Configuration Constants
# Mapped from UPS Rating API Analysis

# ==============================================================================
# Pickup Type Codes
# ==============================================================================
UPS_PICKUP_DAILY = "01"              # Regular scheduled UPS pickup (Default). Invalid code defaults to this.
UPS_PICKUP_CUSTOMER_COUNTER = "03"   # Package dropped at UPS counter
UPS_PICKUP_ONE_TIME = "06"           # Single, ad-hoc pickup
UPS_PICKUP_LETTER_CENTER = "19"      # UPS Letter Center drop-off
UPS_PICKUP_AIR_SERVICE_CENTER = "20" # UPS Air Service Center drop-off

# ==============================================================================
# Rate Type Codes
# ==============================================================================
UPS_RATE_SHIPPER_NUMBER = "00"       # Shipper Number Rates (Contract / discounted pricing). Requires ShipperNumber.
UPS_RATE_DAILY = "01"                # Daily Rates (Standard account pricing)
UPS_RATE_RETAIL = "04"               # Retail Rates (Walk-in / UPS Store)
UPS_RATE_REGIONAL = "05"             # Regional Rates (Special programs)
UPS_RATE_GENERAL_LIST = "06"         # General List Rates (Reference pricing)
UPS_RATE_STANDARD_LIST = "53"        # Standard List Rates (Public list pricing)

# ==============================================================================
# Shipment Indication Types (Access Point)
# ==============================================================================
UPS_INDICATION_HOLD_FOR_PICKUP = "01"       # Hold for Pickup at UPS Access Point (Customer collects)
UPS_INDICATION_ACCESS_POINT_DELIVERY = "02" # UPS Access Point Delivery (Delivered to AP instead of home)

# ==============================================================================
# Payment Types
# ==============================================================================
UPS_PAYMENT_TYPE_TRANSPORTATION = "01" # The shipping cost itself
UPS_PAYMENT_TYPE_DUTIES_TAXES = "02"   # Customs, VAT, or import duties

# ==============================================================================
# FRS Payment Information Types (Freight)
# ==============================================================================
UPS_FRS_PAYMENT_PREPAID = "01"         # Shipper pays (like BillShipper)
UPS_FRS_PAYMENT_FREIGHT_COLLECT = "02" # Receiver pays (like BillReceiver)
UPS_FRS_PAYMENT_BILL_THIRD_PARTY = "03" # Third party pays

# ==============================================================================
# Service Codes - Domestic (US)
# ==============================================================================
UPS_SERVICE_NEXT_DAY_AIR = "01"        # Fastest overnight delivery
UPS_SERVICE_2ND_DAY_AIR = "02"         # 2-day guaranteed delivery
UPS_SERVICE_GROUND = "03"              # Standard ground shipping
UPS_SERVICE_3_DAY_SELECT = "12"        # Delivery within 3 business days
UPS_SERVICE_NEXT_DAY_AIR_SAVER = "13"  # Overnight, slightly slower/cheaper than 01
UPS_SERVICE_NEXT_DAY_AIR_EARLY = "14"  # Early morning next-day delivery
UPS_SERVICE_2ND_DAY_AIR_AM = "59"      # Guaranteed 2nd day delivery in the morning
UPS_SERVICE_HEAVY_GOODS = "75"         # For very heavy shipments

# ==============================================================================
# Service Codes - International
# ==============================================================================
UPS_SERVICE_WORLDWIDE_EXPRESS = "07"           # Fast international delivery
UPS_SERVICE_WORLDWIDE_EXPEDITED = "08"         # Slightly slower, less expensive
UPS_SERVICE_STANDARD = "11"                    # Economy international service
UPS_SERVICE_WORLDWIDE_EXPRESS_PLUS = "54"      # Premium international delivery
UPS_SERVICE_SAVER = "65"                       # International cheaper express
UPS_SERVICE_WORLDWIDE_EXPRESS_FREIGHT = "96"   # For large international freight shipments
UPS_SERVICE_WORLDWIDE_EXPRESS_FREIGHT_MIDDAY = "71" # Midday delivery for international freight

# ==============================================================================
# Packaging Type Codes
# ==============================================================================
UPS_PACKAGING_LETTER = "01"            # UPS Letter (documents only)
UPS_PACKAGING_BOX = "02"               # Regular box (customer-supplied) - MOST COMMON
UPS_PACKAGING_TUBE = "03"              # Tube
UPS_PACKAGING_PAK = "04"               # UPS Pak
UPS_PACKAGING_10KG_BOX = "10"          # UPS 10kg Box
UPS_PACKAGING_25KG_BOX = "25"          # UPS 25kg Box
UPS_PACKAGING_EXPRESS_BOX = "21"       # Express Box (generic)
UPS_PACKAGING_EXPRESS_BOX_SMALL = "26" # Small Express Box
UPS_PACKAGING_EXPRESS_BOX_MEDIUM = "27" # Medium Express Box
UPS_PACKAGING_EXPRESS_BOX_LARGE = "28" # Large Express Box
UPS_PACKAGING_PALLET = "30"            # Pallet (freight)


 
# ==============================================================================
# Simple Rate Sizes (Flat Rate)
# ==============================================================================
UPS_SIMPLE_RATE_XS = "XS"              # Extra Small
UPS_SIMPLE_RATE_S = "S"                # Small
UPS_SIMPLE_RATE_M = "M"                # Medium
UPS_SIMPLE_RATE_L = "L"                # Large
UPS_SIMPLE_RATE_XL = "XL"              # Extra Large

# ==============================================================================
# UPS Premier Categories (Healthcare/Priority)
# ==============================================================================
UPS_PREMIER_SILVER = "01"
UPS_PREMIER_GOLD = "02"
UPS_PREMIER_PLATINUM = "03"

# ==============================================================================
# Units of Measurement
# ==============================================================================
UPS_UNIT_LBS = "LBS"                   # Pounds
UPS_UNIT_KGS = "KGS"                   # Kilograms
UPS_UNIT_INCHES = "IN"                 # Inches
UPS_UNIT_CENTIMETERS = "CM"            # Centimeters

# ==============================================================================
# Package Service Options (Flags/Keys)
# ==============================================================================
UPS_OPTION_DELIVERY_CONFIRMATION = "DeliveryConfirmation"
UPS_OPTION_COD = "COD"
UPS_OPTION_DECLARED_VALUE = "DeclaredValue"
UPS_OPTION_SHIPPER_RELEASE = "ShipperReleaseIndicator"
UPS_OPTION_ADDITIONAL_HANDLING = "AdditionalHandlingIndicator"

# ==============================================================================
# Special Indicators (Keys)
# ==============================================================================
UPS_INDICATOR_RESIDENTIAL = "ResidentialAddressIndicator" # Presence = Residential, Missing = Commercial
UPS_INDICATOR_DOCUMENTS_ONLY = "DocumentsOnlyIndicator"   # Presence = Documents
UPS_INDICATOR_LARGE_PACKAGE = "LargePackageIndicator"     # Presence = Large Package
UPS_INDICATOR_OVERSIZE = "OversizeIndicator"              # Presence = Oversized
UPS_INDICATOR_NEGOTIATED_RATES = "NegotiatedRatesIndicator"

# ==============================================================================
# Billing Options
# ==============================================================================
UPS_BILL_SHIPPER = "BillShipper"
UPS_BILL_RECEIVER = "BillReceiver"
UPS_BILL_THIRD_PARTY = "BillThirdParty"
UPS_BILL_CONSIGNEE = "ConsigneeBilledIndicator"

# ==============================================================================
# Package Bill Type (Content Type)
# ==============================================================================
UPS_PACKAGE_BILL_TYPE_DOCUMENT = "02"          # Document only
UPS_PACKAGE_BILL_TYPE_NON_DOCUMENT = "03"      # Non-Document
UPS_PACKAGE_BILL_TYPE_PALLET_WWEF = "04"       # WWEF Pallet
UPS_PACKAGE_BILL_TYPE_PALLET_DOMESTIC = "07"   # Domestic Pallet