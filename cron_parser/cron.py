import sys
import warnings
ALLOWED_CHARACTERS = set("0123456789,-*/")


class Cron:
    def __init__(self, input_string: str) -> None:
        if not isinstance(input_string, str):
            raise ValueError("Invalid format. The input should be a string.")
        else:
            parts = input_string.split(" ")
            if len(parts) != 5:
                raise ValueError(
                    f"Invalid format. The string should contain exactly 5 parts separated by spaces, got {len(parts)} parts."
                )
            else:
                self.input_string = input_string
                for part in parts:
                    for char in part:
                        if char not in ALLOWED_CHARACTERS:
                            raise ValueError(
                                "Invalid format. The string contains invalid characters."
                            )
                    else:
                        self.raw_minute = parts[0]
                        self.raw_hour = parts[1]
                        self.raw_day_of_month = parts[2]
                        self.raw_month = parts[3]
                        self.raw_day_of_week = parts[4]

                self.minute = Minute(self.raw_minute)
                self.hour = Hour(self.raw_hour)
                self.day_of_month = DayOfMonth(self.raw_day_of_month)
                self.month = Month(self.raw_month)
                self.day_of_week = DayOfWeek(self.raw_day_of_week)

                if 2 in self.month.value:
                    if 30 in self.day_of_month.value or 31 in self.day_of_month.value:
                        warnings.warn(
                            "February cannot have 30 or 31 days in this cron expression."
                        )
                    if 29 in self.day_of_month.value:
                        warnings.warn(
                            "February 29th may not occur every year; ensure this is intended in the cron expression."
                        )

                if any(m in set(self.month.value) for m in set((4, 6, 9, 11))):
                    if 31 in self.day_of_month.value:
                        warnings.warn(
                            "Specified month(s) cannot have 31 days in this cron expression."
                        )
                

    def print_output(self) -> None:
        for part in [self.minute, self.hour, self.day_of_month, self.month, self.day_of_week]:
            if isinstance(part, Part):
                values = " ".join(str(v) for v in part.value)
                f = f"{part.part_name:<14} {values}"
                print(f)

class Part:
    def __init__(
        self, raw_part: str, min_value: int, max_value: int, part_name: str
    ) -> None:
        self.raw_part = raw_part
        self.min_value = min_value
        self.max_value = max_value
        self.part_name = part_name
        self.value = self.parse()

    def parse(self) -> list:
        if "/" in self.raw_part:
            base_str, step_str = self.raw_part.split("/")
            step = int(step_str)
            if "*" in base_str:
                base_parse = Part(
                    raw_part=base_str,
                    min_value=self.min_value,
                    max_value=self.max_value,
                    part_name=self.part_name,
                ).parse()
                return [v for v in base_parse if (v - self.min_value) % step == 0]
            elif "-" in base_str:
                start_base_str, end_base_str = base_str.split("-")
                start_base = int(start_base_str)
                end_base = int(end_base_str)
                if (
                    start_base >= self.min_value
                    and end_base <= self.max_value
                    and start_base < end_base
                ):
                    base_parse = Part(
                        raw_part=base_str,
                        min_value=start_base,
                        max_value=end_base,
                        part_name=self.part_name,
                    ).parse()
                    return [v for v in base_parse if (v - start_base) % step == 0]
                else:
                    raise ValueError(f"Invalid range in base value. Received {base_str} as base for {self.part_name}, expected base value between {self.min_value}-{self.max_value}.")
            else:
                raise ValueError("Invalid format for base value.")

        elif "*" in self.raw_part:
            if self.part_name == "day_of_week":
                return list(range(self.min_value, self.max_value))  # 0-6 for day_of_week if *, start at 0, end at 6 for generation
            return list(range(self.min_value, self.max_value + 1))
        elif "-" in self.raw_part:
            start_str, end_str = self.raw_part.split("-")
            start = int(start_str)
            end = int(end_str)
            if start < self.min_value or end > self.max_value or start > end:
                raise ValueError(f"Invalid range in as {self.part_name}. Received {self.raw_part} as {self.part_name}, expected range between {self.min_value} and {self.max_value}.")
            return list(range(start, end + 1))
        elif "," in self.raw_part:
            values = [int(v) for v in self.raw_part.split(",")]
            for v in values:
                if v < self.min_value or v > self.max_value:
                    raise ValueError(f"Invalid value in {self.part_name}. Received {v} as {self.part_name}, expected value between {self.min_value} and {self.max_value}.")
            return values
        else:
            if int(self.raw_part) < self.min_value or int(self.raw_part) > self.max_value:
                raise ValueError(f"Invalid value in {self.part_name}. Received {self.raw_part} as {self.part_name}, expected value between {self.min_value} and {self.max_value}.")
            return [int(self.raw_part)]


class Minute(Part):
    def __init__(self, raw_part: str) -> None:
        super().__init__(raw_part, 0, 59, part_name="minute")


class Hour(Part):
    def __init__(self, raw_part: str) -> None:
        super().__init__(raw_part, 0, 23, part_name="hour")


class DayOfMonth(Part):
    def __init__(self, raw_part: str) -> None:
        super().__init__(raw_part, 1, 31, part_name="day_of_month")


class Month(Part):
    def __init__(self, raw_part: str) -> None:
        super().__init__(raw_part, 1, 12, part_name="month")


class DayOfWeek(Part):
    def __init__(self, raw_part: str) -> None:
        super().__init__(raw_part, 0, 7, part_name="day_of_week") # Both 0 and 7 represent Sunday
