# SPDX-License-Identifier: Polyform-Noncommercial-1.0.0

"""
target_preferences.py

Stores and manages user-specified target companies and roles for StrongTies.

Classes:
    TargetPreferences
"""

from typing import List, Dict

class TargetPreferences:
    """
    Stores and manages user-specified target companies and roles.

    Attributes
    ----------
    companies : List[str]
        List of target companies.
    roles : List[str]
        List of target roles.

    Methods
    -------
    add_company(company: str) -> None
        Adds a company to the target list if not already present.
    add_role(role: str) -> None
        Adds a role to the target list if not already present.
    to_dict() -> Dict[str, List[str]]
        Returns the preferences as a dictionary.
    matches(connection: Dict) -> bool
        Checks if a connection matches any target company or role.
    """

    def __init__(self, companies: List[str] = None, roles: List[str] = None):
        self.companies = companies or []
        self.roles = roles or []

    def add_company(self, company: str) -> None:
        """Add a company to the target list if not already present."""
        if company not in self.companies:
            self.companies.append(company)

    def add_role(self, role: str) -> None:
        """Add a role to the target list if not already present."""
        if role not in self.roles:
            self.roles.append(role)

    def to_dict(self) -> Dict[str, List[str]]:
        """Return the preferences as a dictionary."""
        return {"companies": self.companies, "roles": self.roles}

    def matches(self, connection: Dict) -> bool:
        """
        Checks if a connection matches any target company or role.

        Parameters
        ----------
        connection : Dict
            Dictionary representing a connection, with keys 'company' and 'role'.

        Returns
        -------
        bool
            True if the connection matches a target company or role, False otherwise.
        """
        return (
            connection.get("company") in self.companies or
            connection.get("role") in self.roles
        )