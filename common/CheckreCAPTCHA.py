# Check for reCAPTCHA
# XUZhengyi, 26/01/2018

import json
try:
    from common import GetHtml
except:
    import GetHtml
try:
    from common import settings
except:
    import settings


def check_reCAPTCHA(res):
    secret = settings.googlerec_key
    url = 'https://www.google.com/recaptcha/api/siteverify';
    post_data = {'secret': secret, 'response': res}
    getter = GetHtml.GetHtml()
    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    getter.set(url, header=header, postData=post_data)
    r = json.loads(getter.get().decode("utf-8"))
    return r['success']


if __name__ == '__main__':
    check_reCAPTCHA("03AA7ASh1W_T6qxR80xeSgC62wVw6CP3W7DfvFVcD9-sNN_xMeNxNDebEz05L3uj9sugT7NSYQFhRR8DlFRNQTaLPceXX6RJ1vDdj6Gzbuz-kwNu-jhAOuZ44DvkjP3wkuSOiNKcMNW2A-rfLXU2j66FF7_Y8YnwnNXNGCrOI_llVg006n6XFPhVxWC0FaBXMbuLSY82xwVzsUZkxk1r1TrRw2i7fPLp83F9443kf-lx_WWROHJQzCa_3rizFluw-0ar0byVw1Lz8aEtH2WBl-RLTeT6cC-tS0HXSv9Wk8G6wkLLMOjiexyr2JRaTfQeKliuVcpp78GTyMjR8M_8xnRipybLVmwK87SklTUiPcmbMlm1cYLkKNYkfQA1UaDZ8VEXndR9yUBIPaa4fcfsiIAKxA_FIliDUunqFixzEQ34SftohjYJyaluU")
