"""
Suite de Pruebas Unitarias para PyEDC.
"""

import unittest
from pyedc.modules.calculator.subnetting import calculate_subnet_info, calculate_vlsm
from pyedc.modules.calculator.mtu_mss import calculate_mtu_mss
from pyedc.modules.calculator.optics import calculate_optical_budget
from pyedc.modules.calculator.fabric_design import calculate_spine_leaf

from pyedc.modules.automator.matrix_parser import parse_cli_matrix, parse_iana_ports
from pyedc.modules.automator.transpiler import translate_command, find_equivalent_task
from pyedc.modules.automator.generator import generate_device_config

from pyedc.modules.examiner.parser import load_all_question_banks
from pyedc.modules.copilot.indexer import KnowledgeIndexer
from pyedc.modules.copilot.retriever import KnowledgeRetriever


class TestPyEDC(unittest.TestCase):

    def test_subnet_info(self):
        info = calculate_subnet_info("192.168.1.0/24")
        self.assertEqual(info["network"], "192.168.1.0")
        self.assertEqual(info["broadcast"], "192.168.1.255")
        self.assertEqual(info["usable_hosts"], 254)
        self.assertEqual(info["netmask"], "255.255.255.0")
        self.assertEqual(info["wildcard"], "0.0.0.255")

    def test_vlsm(self):
        reqs = [("Ventas", 50), ("Sistemas", 20), ("DMZ", 10), ("WAN", 2)]
        res = calculate_vlsm("192.168.10.0/24", reqs)
        self.assertEqual(len(res["subnets"]), 4)
        self.assertEqual(res["subnets"][0]["prefix"], 26)  # 50 hosts -> /26 (62 usables)
        self.assertEqual(res["subnets"][1]["prefix"], 27)  # 20 hosts -> /27 (30 usables)
        self.assertEqual(res["subnets"][2]["prefix"], 28)  # 10 hosts -> /28 (14 usables)
        self.assertEqual(res["subnets"][3]["prefix"], 30)  # 2 hosts -> /30 (2 usables)
        self.assertGreaterEqual(res["free_addresses_remaining"], 0)

    def test_mtu_mss(self):
        res = calculate_mtu_mss(base_mtu=1500, active_encapsulations=["ipsec_esp"])
        # Base: 1500 - 72 (IPsec) = 1428. TCP MSS = 1428 - 20 (IP) - 20 (TCP) = 1388
        self.assertEqual(res["effective_ip_mtu"], 1428)
        self.assertEqual(res["recommended_tcp_mss"], 1388)
        self.assertIn("cisco", res["cli_remediation"])

    def test_optical_budget(self):
        # Enlace de 5 km con 10GBASE-LR (atenuación viable)
        res = calculate_optical_budget(distance_km=5.0, fiber_type="OS2_1310", transceiver_model="10GBASE-LR", safety_margin=2.0)
        self.assertIn("VIABLE", res["status"])
        self.assertGreater(res["operating_margin_db"], 0)

    def test_fabric_design(self):
        res = calculate_spine_leaf(num_leafs=4, downlinks_per_leaf=48, uplinks_per_leaf=4)
        self.assertEqual(res["required_spines"], 4)
        self.assertEqual(res["oversubscription_ratio"], 3.0)  # (48*25) / (4*100) = 1200 / 400 = 3.0

    def test_cli_matrix_parser(self):
        matrix = parse_cli_matrix()
        self.assertGreater(len(matrix), 5)
        iana = parse_iana_ports()
        self.assertGreater(len(iana), 10)

    def test_transpiler(self):
        # Traducir switchport mode trunk de Cisco a Huawei
        res = translate_command("switchport mode trunk", "cisco", "huawei")
        self.assertIn("port link-type trunk", res["translated"])

    def test_generator(self):
        cfg = generate_device_config("vlan", "cisco", {"vlan_id": 20, "name": "USUARIOS"})
        self.assertIn("vlan 20", cfg)
        self.assertIn("name USUARIOS", cfg)

    def test_question_parser(self):
        questions = load_all_question_banks()
        self.assertGreaterEqual(len(questions), 10)
        q1 = questions[0]
        self.assertIn("A", q1.options)
        self.assertTrue(len(q1.correct_answer) == 1)

    def test_copilot_retriever(self):
        retriever = KnowledgeRetriever()
        results = retriever.search("RFC 7348 VXLAN", top_k=3)
        self.assertGreater(len(results), 0)
        top_chunk, score = results[0]
        self.assertIn("RFC 7348", top_chunk.content.upper() + "".join(top_chunk.rfcs_mentioned))

    def test_glossary_engine(self):
        from pyedc.modules.glossary.glossary_engine import GlossaryEngine
        engine = GlossaryEngine()
        self.assertGreaterEqual(len(engine.terms), 50)
        bgp_terms = engine.search("BGP")
        self.assertGreater(len(bgp_terms), 0)
        self.assertIn("BGP", bgp_terms[0].term)

    def test_troubleshooter_engine(self):
        from pyedc.modules.troubleshooter.troubleshooter import TroubleshooterEngine
        engine = TroubleshooterEngine()
        cases = engine.get_all_cases()
        self.assertGreaterEqual(len(cases), 5)
        tcp_case = engine.get_case("tcp_retransmissions")
        self.assertIsNotNone(tcp_case)
        self.assertIn("retransmission", tcp_case.wireshark_display_filter)

    def test_rfc_catalog(self):
        from pyedc.modules.standards.rfc_catalog import RFCCatalog
        catalog = RFCCatalog()
        self.assertGreaterEqual(len(catalog.rfcs), 10)
        results = catalog.search("791")
        self.assertGreater(len(results), 0)
        self.assertEqual(results[0].number, 791)

    def test_lab_catalog(self):
        from pyedc.modules.labs.lab_catalog import LabCatalog
        catalog = LabCatalog()
        blocks = catalog.get_all_blocks()
        self.assertEqual(len(blocks), 10)
        evpn_blocks = catalog.search_labs("EVPN")
        self.assertGreater(len(evpn_blocks), 0)


if __name__ == "__main__":
    unittest.main()

