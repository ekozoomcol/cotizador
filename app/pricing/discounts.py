from dataclasses import dataclass


@dataclass
class DiscountsConfig:
    """
    Espejo a H49, I49, J49, K49, L49
    """

    def dto_altura_rollo(self, E5: float) -> float:
        # H49: =SI(Y(E5>=60; E5<=67); 4; 0)
        return 4 if (E5 >= 60 and E5 <= 67) else 0

    def dto_tuco_pq(self, E5: float) -> float:
        # I49: =SI(Y(E5>=0; E5<=59); 6; 0)
        return 6 if (E5 >= 0 and E5 <= 59) else 0

    def dto_poco_desperdicio(self, F5: float) -> float:
        # J49: =SI(Y(F5>=0; F5<21); 4,0; 0)
        return 4.0 if (F5 >= 0 and F5 < 21) else 0.0

    def dto_cola_produccion(self, P2: float) -> float:
        # K49: =SI(P2<30000; 3; 0)
        return 3 if (P2 < 30000) else 0

    def dto_final_L49(self, E5: float, F5: float, P2: float) -> float:
        # L49: =MAX(H49:K49)
        return max(
            self.dto_altura_rollo(E5),
            self.dto_tuco_pq(E5),
            self.dto_poco_desperdicio(F5),
            self.dto_cola_produccion(P2),
        )