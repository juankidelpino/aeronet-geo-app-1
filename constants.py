JAP_DEV_FLAG = False
JAP_DEBUG_FLAG = True
JAP_TESTING_FLAG = False
JAP_SONAR_URL = "https://aeronetsandbox.sonar.software/api/v1" if JAP_DEV_FLAG else "https://aeronet.sonar.software/api/v1"
CNMAESTRO_URL = 'https://173.243.80.206/api/v2'
NEW_CNMAESTRO_URL = 'https://cnmaestro.aeronetpr.com/api/v2'
PBX_URL = 'https://aerovoip.aeronetpr.com'
JAP_SONAR_VOIP_LOCAL_PREFIXES = ["1", "787", "939"]
JAP_SONAR_TAX_IDS = [1, 2] if JAP_DEV_FLAG else [2, 6]
SONAR_ACCOUNT_TYPE_ID_SET_VOIP = {5, 6} if JAP_DEV_FLAG else {9, 10, 11}
PIPE_URL = "https://aeronet.pipedrive.com/v1"