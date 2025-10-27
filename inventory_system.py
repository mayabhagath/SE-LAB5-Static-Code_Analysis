"""
Inventory Management System
"""
from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class Inventory:
    """Simple inventory manager."""

    def __init__(self, initial: Optional[Dict[str, int]] = None) -> None:
        self._stock: Dict[str, int] = {}
        if initial:
            for k, v in initial.items():
                self._stock[str(k)] = int(v)

    def add_item(self, item: str, qty: int) -> None:
        """Add quantity of item to inventory. qty must be non-negative int."""
        if not isinstance(item, str):
            raise TypeError("item must be a string")
        if not isinstance(qty, int):
            raise TypeError("qty must be an int")
        if qty < 0:
            raise ValueError("qty must be non-negative for add_item")
        current = self._stock.get(item, 0)
        self._stock[item] = current + qty
        logger.info("%s: Added %d of %s", datetime.now(), qty, item)

    def remove_item(self, item: str, qty: int) -> None:
        """Remove quantity of item. If item not present or qty invalid, log/raise."""
        if not isinstance(item, str):
            raise TypeError("item must be a string")
        if not isinstance(qty, int):
            raise TypeError("qty must be an int")
        if qty < 0:
            raise ValueError("qty must be non-negative for remove_item")
        if item not in self._stock:
            logger.warning("Attempt to remove non-existent item: %s", item)
            raise KeyError(f"{item} not in inventory")
        if self._stock[item] <= qty:
            # remove item entirely
            del self._stock[item]
            logger.info("%s: Removed %d of %s (item deleted)", datetime.now(), qty, item)
        else:
            self._stock[item] -= qty
            logger.info("%s: Removed %d of %s", datetime.now(), qty, item)

    def get_qty(self, item: str) -> int:
        """Return quantity of item, or 0 if not present."""
        if not isinstance(item, str):
            raise TypeError("item must be a string")
        return self._stock.get(item, 0)

    def check_low_items(self, threshold: int = 5) -> List[str]:
        """Return a list of items with quantity below threshold."""
        if not isinstance(threshold, int):
            raise TypeError("threshold must be an int")
        return [name for name, qty in self._stock.items() if qty < threshold]

    def print_report(self) -> None:
        """Log a simple report of items and quantities."""
        logger.info("Items Report")
        for name, qty in self._stock.items():
            logger.info("%s -> %d", name, qty)

    def save_data(self, file_path: str = "inventory.json") -> None:
        """Save inventory to file safely. Existing file will be overwritten."""
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(self._stock, f, ensure_ascii=False, indent=2)
            logger.info("Inventory saved to %s", file_path)
        except OSError:
            logger.exception("Failed to write inventory to %s", file_path)
            raise

    def load_data(self, file_path: str = "inventory.json") -> None:
        """Load inventory from file. If file missing, keep empty inventory."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                logger.error("Inventory file format invalid: expected dict")
                return
            # enforce types
            self._stock = {str(k): int(v) for k, v in data.items()}
            logger.info("Inventory loaded from %s", file_path)
        except FileNotFoundError:
            logger.info("No inventory file found at %s; starting fresh", file_path)
        except json.JSONDecodeError:
            logger.exception("Invalid JSON in inventory file %s", file_path)
        except (TypeError, ValueError):
            logger.exception("Inventory file %s contains invalid values", file_path)

    @property
    def stock(self) -> Dict[str, int]:
        """Expose a copy for read-only access."""
        return dict(self._stock)


def configure_logging(level: int = logging.INFO) -> None:
    """Configure module-level logging."""
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s - %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)


def main() -> None:
    configure_logging()
    inv = Inventory()
    inv.add_item("apple", 10)
    # Proper removal using remove_item
    inv.remove_item("apple", 3)
    try:
        inv.add_item("banana", 2)
    except Exception:
        logger.exception("Failed to add banana")

    # Demonstrate type-check error being raised (commented for normal run)
    # inv.add_item(123, "ten")  # would raise TypeError

    logger.info("Apple stock: %d", inv.get_qty("apple"))
    logger.info("Low items: %s", inv.check_low_items())
    inv.save_data()
    inv.load_data()
    inv.print_report()


if __name__ == "__main__":
    main()
