from dataclasses import dataclass


@dataclass
class Job:
    url: str
    title: str
    salary_from: int
    salary_to: int
    currency: str
    description: str

    @property
    def salary(self) -> str:
        if self.salary_from == 0 and self.salary_to == 0:
            return "Договорная"
        elif self.salary_to == 0:
            return f"От {self.salary_from}{self.currency}"
        elif self.salary_from == 0:
            return f"До {self.salary_to}{self.currency}"
        else:
            return f"От {self.salary_from}{self.currency} до {self.salary_to}{self.currency}"
