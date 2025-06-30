import sys
from pathlib import Path
from data_analytics.data_analytics import ParseDataAnalytics

if __name__ == "__main__":
    # Los Andes, Calle Larga, Til Til y Colina

    words = ["Los Andes", "Calle Larga", "Til Til", "Colina"]
    pda = ParseDataAnalytics(Path(sys.argv[1]), words)

    print("High Impact Media  ---------------------------")
    print()
    pda.high_impact_media()

    print("Medium Impact Media  ---------------------------")
    print()
    pda.medium_impact_media()

    print("Low Impact Media  ---------------------------")
    print()
    pda.low_impact_media()
