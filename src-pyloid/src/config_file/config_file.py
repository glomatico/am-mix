from enum import Enum
from pathlib import Path
from typing import Any
from .types import Config

import yaml

from .constants import DEFAULT_SETTINGS


class ConfigFile:
    def __init__(self):
        self._initialize_path()
        self._initialize_config()

    def _initialize_path(self) -> None:
        self.config_path = Path.home() / ".am-mix" / "config.yml"
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

    def _initialize_config(self) -> None:
        if self.config_path.exists():
            with self.config_path.open("r") as file:
                self.json_config = yaml.safe_load(file)
        else:
            self.json_config = {}

        self.config = Config()
        for key, default_setting in DEFAULT_SETTINGS.__dict__.items():
            if key in self.json_config:
                self.config.__dict__[key] = self._parse_config(
                    key,
                    default_setting.is_list,
                    default_setting.nullable,
                    default_setting.data_type,
                    self.json_config[key],
                )
            else:
                self.config.__dict__[key] = default_setting.default_value
                self.json_config[key] = self._serialize_config(
                    default_setting.default_value,
                    default_setting.is_list,
                )

    def get_json_config(self) -> dict[str, Any]:
        return self.json_config

    def get_config(self) -> Config:
        return self.config

    def exists(self) -> bool:
        return self.config_path.exists()

    def save(self) -> None:
        with self.config_path.open("w") as file:
            yaml.dump(self.json_config, file)

    def update(
        self,
        update: dict[str, Any],
    ) -> None:
        for key, value in update.items():
            if key not in DEFAULT_SETTINGS.__dict__:
                continue

            config_option = DEFAULT_SETTINGS.__dict__[key]

            self.config.__dict__[key] = self._parse_config(
                key,
                config_option.is_list,
                config_option.nullable,
                config_option.data_type,
                value,
            )

            self.json_config[key] = self._serialize_config(
                self.config.__dict__[key],
                config_option.is_list,
            )

        self.save()

    def _parse_config(
        self,
        key: str,
        is_list: bool,
        nullable: bool,
        data_type: type,
        value: Any,
    ) -> Any:
        if (value is None or value == "") and not nullable:
            raise ValueError(f"Value cannot be null for key: {key}")

        if value is None:
            return None

        if is_list:
            return [data_type(item) for item in value]

        return data_type(value)

    def _serialize_config(self, value: Any, is_list: bool) -> Any:
        if value is None:
            return None

        if is_list:
            return [item.value if isinstance(item, Enum) else item for item in value]

        return value.value if isinstance(value, Enum) else value
