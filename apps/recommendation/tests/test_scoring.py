import itertools

from django.test import TestCase

from apps.smartphones.models import Brand, Chipset, Smartphone
from apps.recommendation.scoring import (  # adjust import path to match your module
    _scale,
    battery_score,
    calculate_and_save_scores,
    calculate_and_save_scores_bulk,
    camera_score,
    compute_scores,
    display_score,
    get_phone_scores,
    performance_score,
    REFERENCE_MAX,
)


class ScoringTestCase(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.brand = Brand.objects.create(name="Samsung")
        cls.chipset = Chipset.objects.create(
            name="Snapdragon 8 Elite",
            antutu_score=1100000,
            geekbench_multi=9500,
        )

    DEFAULT_PHONE_KWARGS = dict(
        name="Galaxy S25 Ultra",
        ram_gb=12,
        storage_gb=256,
        storage_type="ufs4_0",
        battery_mah=5000,
        fast_charging_w=45,
        display_refresh_hz=120,
        display_ppi=505,
        display_type="AMOLED",
        main_camera_mp=200,
    )

    def _make_phone(self, chipset=None, **overrides):
       
        kwargs = {**self.DEFAULT_PHONE_KWARGS, **overrides}
        return Smartphone.objects.create(
            brand=self.brand,
            chipset=chipset or self.chipset,
            **kwargs,
        )

    _chipset_names = itertools.count()

    def _make_chipset(self, **overrides):
        kwargs = dict(
            name=f"Chipset-{next(self._chipset_names)}",
            antutu_score=1000000,
            geekbench_multi=9000,
        )
        kwargs.update(overrides)
        return Chipset.objects.create(**kwargs)


    def test_scale_none_returns_zero(self):
        self.assertEqual(_scale(None, 100), 0)

    def test_scale_clamps_at_100(self):
        
        self.assertEqual(_scale(500, 100), 100)

    def test_scale_zero_value(self):
        self.assertEqual(_scale(0, 100), 0)

   

    def test_performance_score_in_range(self):
        phone = self._make_phone()
        score = performance_score(phone)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)

    def test_performance_score_matches_formula(self):
        chipset = self._make_chipset(antutu_score=1100000)
        phone = self._make_phone(chipset=chipset, ram_gb=12, storage_type="ufs4_0")

        cpu = (1100000 / REFERENCE_MAX["antutu"]) * 100
        ram = (12 / REFERENCE_MAX["ram"]) * 100
        storage = (4 / REFERENCE_MAX["storage_speed"]) * 100
        expected = round(cpu * 0.6 + ram * 0.25 + storage * 0.15, 2)

        self.assertEqual(performance_score(phone), expected)

    def test_performance_score_monotonic_inputs(self):
        cases = [
            ("antutu_score", dict(chipset=self._make_chipset(antutu_score=1000000)),
             dict(chipset=self._make_chipset(antutu_score=2000000))),
            ("ram_gb", dict(ram_gb=8), dict(ram_gb=12)),
            ("storage_type", dict(storage_type="ufs2_2"), dict(storage_type="ufs4_0")),
        ]
        for label, low_kwargs, high_kwargs in cases:
            with self.subTest(field=label):
                low = self._make_phone(**low_kwargs)
                high = self._make_phone(**high_kwargs)
                self.assertGreater(performance_score(high), performance_score(low))

    def test_performance_score_unknown_storage_type_defaults_to_rank_one(self):
        known = self._make_phone(storage_type="emmc")  
        unknown = self._make_phone(storage_type="some_future_storage")  
        self.assertEqual(performance_score(known), performance_score(unknown))

    

    def test_battery_score_in_range(self):
        phone = self._make_phone()
        score = battery_score(phone)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)

    def test_battery_score_matches_formula(self):
        phone = self._make_phone(battery_mah=4000, fast_charging_w=45)

        capacity = (4000 / REFERENCE_MAX["battery"]) * 100
        charging = (45 / REFERENCE_MAX["charging"]) * 100
        expected = round(capacity * 0.7 + charging * 0.3, 2)

        self.assertEqual(battery_score(phone), expected)

    def test_battery_score_monotonic_inputs(self):
        cases = [
            ("battery_mah", dict(battery_mah=4000), dict(battery_mah=5000)),
            ("fast_charging_w", dict(fast_charging_w=45), dict(fast_charging_w=55)),
        ]
        for label, low_kwargs, high_kwargs in cases:
            with self.subTest(field=label):
                low = self._make_phone(**low_kwargs)
                high = self._make_phone(**high_kwargs)
                self.assertGreater(battery_score(high), battery_score(low))

    
    def test_display_score_in_range(self):
        phone = self._make_phone()
        score = display_score(phone)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)

    def test_display_score_matches_formula(self):
        phone = self._make_phone(
            display_refresh_hz=120, display_ppi=505, display_type="S-AMOLED"
        )

        refresh = (120 / REFERENCE_MAX["refresh"]) * 100
        ppi = (505 / REFERENCE_MAX["ppi"]) * 100
        panel = (5 / REFERENCE_MAX["display_type"]) * 100
        expected = round(refresh * 0.35 + ppi * 0.35 + panel * 0.30, 2)

        self.assertEqual(display_score(phone), expected)

    def test_display_score_monotonic_inputs(self):
        cases = [
            ("display_refresh_hz", dict(display_refresh_hz=60), dict(display_refresh_hz=120)),
            ("display_ppi", dict(display_ppi=500), dict(display_ppi=505)),
            ("display_type", dict(display_type="OLED"), dict(display_type="S-AMOLED")),
        ]
        for label, low_kwargs, high_kwargs in cases:
            with self.subTest(field=label):
                low = self._make_phone(**low_kwargs)
                high = self._make_phone(**high_kwargs)
                self.assertGreater(display_score(high), display_score(low))

    def test_display_score_unknown_display_type_defaults_to_rank_one(self):
       
        known = self._make_phone(display_type="LCD")  
        unknown = self._make_phone(display_type="FUTURE")  
        self.assertEqual(display_score(known), display_score(unknown))

    

    def test_camera_score_in_range(self):
        phone = self._make_phone()
        score = camera_score(phone)
        self.assertGreater(score, 0)
        self.assertLessEqual(score, 100)

    def test_camera_score_matches_formula(self):
        phone = self._make_phone(main_camera_mp=180)
        megapixel = (180 / REFERENCE_MAX["camera"]) * 100
        expected = round(megapixel * 0.85, 2)
        self.assertEqual(camera_score(phone), expected)

    def test_camera_score_monotonic_megapixels(self):
        low = self._make_phone(main_camera_mp=150)
        high = self._make_phone(main_camera_mp=200)
        self.assertGreater(camera_score(high), camera_score(low))

    def test_camera_score_caps_at_100_above_reference_max(self):
        
        phone = self._make_phone(main_camera_mp=300)
        self.assertLessEqual(camera_score(phone), 100)

    

    def test_compute_scores_returns_all_four_fields_and_matches_individual_calls(self):
        phone = self._make_phone()
        scores = compute_scores(phone)

        self.assertEqual(
            set(scores.keys()),
            {"performance_score", "battery_score", "display_score", "camera_score"},
        )
        self.assertEqual(scores["performance_score"], performance_score(phone))
        self.assertEqual(scores["battery_score"], battery_score(phone))
        self.assertEqual(scores["display_score"], display_score(phone))
        self.assertEqual(scores["camera_score"], camera_score(phone))

    def test_compute_scores_runs_no_queries(self):
       
        phone = self._make_phone()
        with self.assertNumQueries(0):
            compute_scores(phone)

   
    def test_calculate_and_save_scores_persists_all_four_fields(self):
        phone = self._make_phone()
        calculate_and_save_scores(phone)

        phone.refresh_from_db()
        self.assertEqual(phone.performance_score, performance_score(phone))
        self.assertEqual(phone.battery_score, battery_score(phone))
        self.assertEqual(phone.display_score, display_score(phone))
        self.assertEqual(phone.camera_score, camera_score(phone))

   

    def test_calculate_and_save_scores_bulk_persists_for_every_phone(self):
        phone_a = self._make_phone(main_camera_mp=150)
        phone_b = self._make_phone(main_camera_mp=200)

        calculate_and_save_scores_bulk([phone_a, phone_b])

        phone_a.refresh_from_db()
        phone_b.refresh_from_db()
        self.assertIsNotNone(phone_a.performance_score)
        self.assertIsNotNone(phone_b.performance_score)
        self.assertNotEqual(phone_a.camera_score, phone_b.camera_score)

    def test_calculate_and_save_scores_bulk_accepts_a_generator(self):
        phone = self._make_phone()
        calculate_and_save_scores_bulk(p for p in [phone])

        phone.refresh_from_db()
        self.assertIsNotNone(phone.performance_score)

    def test_calculate_and_save_scores_bulk_empty_list_does_not_error(self):
        calculate_and_save_scores_bulk([])  

    

    def test_get_phone_scores_reads_stored_fields(self):
        phone = self._make_phone()
        calculate_and_save_scores(phone)
        phone.refresh_from_db()

        result = get_phone_scores(phone)

        self.assertEqual(
            result,
            {
                "performance": phone.performance_score,
                "battery": phone.battery_score,
                "display": phone.display_score,
                "camera": phone.camera_score,
            },
        )