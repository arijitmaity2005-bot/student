from django.core.cache import cache
from django.test import RequestFactory, TestCase, override_settings

from login.utils import (
    OTP_SEND_LIMIT_PER_IP,
    get_client_ip,
    record_otp_send,
    sanitize_for_output,
)


@override_settings(CACHES={
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'otp-limit-tests',
    }
})
class OTPRateLimitTests(TestCase):
    def setUp(self):
        cache.clear()

    def test_otp_send_limit_is_three_per_ip(self):
        request = RequestFactory().post('/register/submit/')
        request.META['REMOTE_ADDR'] = '203.0.113.45'

        for _ in range(OTP_SEND_LIMIT_PER_IP):
            self.assertTrue(record_otp_send(request))

        self.assertFalse(record_otp_send(request))
        self.assertEqual(get_client_ip(request), '203.0.113.45')

    def test_sanitize_for_output_removes_script_tags(self):
        self.assertEqual(
            sanitize_for_output('<script>alert(1)</script>hello'),
            'alert(1)hello'
        )
