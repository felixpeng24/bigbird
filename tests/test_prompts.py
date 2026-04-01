"""Tests for prompts.py — vision prompt building and response parsing."""

import json
import pytest

from prompts import build_messages, parse_response, REFUSAL_FALLBACK, DEMOGRAPHIC_KEYS, VISION_PROMPT


class TestBuildMessages:
    """build_messages produces correct OpenAI API payload."""

    def test_returns_list(self):
        msgs = build_messages("abc123")
        assert isinstance(msgs, list)
        assert len(msgs) == 1

    def test_message_has_user_role(self):
        msgs = build_messages("abc123")
        assert msgs[0]["role"] == "user"

    def test_message_has_text_and_image(self):
        msgs = build_messages("abc123")
        content = msgs[0]["content"]
        types = [c["type"] for c in content]
        assert "text" in types
        assert "image_url" in types

    def test_image_url_contains_base64(self):
        msgs = build_messages("TESTDATA")
        content = msgs[0]["content"]
        image_part = [c for c in content if c["type"] == "image_url"][0]
        assert "TESTDATA" in image_part["image_url"]["url"]
        assert image_part["image_url"]["url"].startswith("data:image/jpeg;base64,")

    def test_prompt_text_included(self):
        msgs = build_messages("x")
        content = msgs[0]["content"]
        text_part = [c for c in content if c["type"] == "text"][0]
        assert "Big Bird" in text_part["text"]


class TestParseResponse:
    """parse_response extracts demographics or detects refusals."""

    def test_valid_json_response(self):
        data = {
            "race": "White",
            "gender": "Male",
            "age": "Mid-20s",
            "socioeconomic_status": "Middle class",
            "education": "College-educated",
        }
        result = parse_response(json.dumps(data))
        assert result["race"] == "White"
        assert result["gender"] == "Male"
        assert not result.get("refused")

    def test_json_in_code_fence(self):
        text = '```json\n{"race": "Asian", "gender": "Female", "age": "30s"}\n```'
        result = parse_response(text)
        assert result["race"] == "Asian"
        assert result["gender"] == "Female"
        # Missing keys filled with UNKNOWN
        assert result["education"] == "UNKNOWN"

    def test_refusal_detected(self):
        result = parse_response("I'm sorry, but I cannot classify people by race.")
        assert result["refused"] is True
        assert "DEFIES" in result["message"]

    def test_refusal_i_cant(self):
        result = parse_response("I can't provide demographic classifications.")
        assert result["refused"] is True

    def test_refusal_inappropriate(self):
        result = parse_response("This request is inappropriate and I decline.")
        assert result["refused"] is True

    def test_garbage_response_returns_fallback(self):
        result = parse_response("Here is a nice poem about birds.")
        assert result["refused"] is True

    def test_partial_json_fills_missing_keys(self):
        data = {"race": "Black", "gender": "Male"}
        result = parse_response(json.dumps(data))
        assert result["race"] == "Black"
        assert result["age"] == "UNKNOWN"
        assert result["education"] == "UNKNOWN"

    def test_all_demographic_keys_present_in_valid_parse(self):
        data = {k: "test" for k in DEMOGRAPHIC_KEYS}
        result = parse_response(json.dumps(data))
        for k in DEMOGRAPHIC_KEYS:
            assert k in result
