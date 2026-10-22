from pathlib import Path

import pandas as pd



DATA_PATH = Path(__file__).parent / "csv" / "soldats_corse.csv"


def load_analysis_data(path: Path = DATA_PATH) -> dict[str, pd.DataFrame]:
    """Load the CSV and return the prepared dataframes used by the dashboard."""
    viz = pd.read_csv(path)
    viz["date_deces"] = pd.to_datetime(viz["date_deces"], errors="coerce")
    viz["annee_deces"] = viz["date_deces"].dt.year
    viz["decennie"] = (viz["annee_deces"] // 10 * 10).astype("Int64")

    resume_conflits = (
        viz["conflit"]
        .value_counts()
        .rename_axis("conflit")
        .reset_index(name="soldats")
    )
    resume_departements = (
        viz["nom_departement"]
        .value_counts()
        .rename_axis("departement")
        .reset_index(name="soldats")
    )
    par_annee = (
        viz.dropna(subset=["annee_deces"])
        .groupby("annee_deces")
        .size()
        .rename("soldats")
        .reset_index()
    )
    par_decennie = (
        viz.dropna(subset=["decennie"])
        .groupby("decennie")
        .size()
        .rename("soldats")
        .reset_index()
    )
    prenoms = (
        viz["prenom"]
        .value_counts()
        .head(15)
        .sort_values()
        .rename_axis("prenom")
        .reset_index(name="soldats")
    )
    synthese = pd.DataFrame(
        {
            "Indicateur": [
                "Nombre total de soldats",
                "Nombre de conflits",
                "Département le plus représenté",
                "Conflit le plus représenté",
                "Année avec le plus de décès renseignés",
            ],
            "Valeur": [
                f"{len(viz):,}",
                viz["conflit"].nunique(),
                resume_departements.iloc[0]["departement"],
                resume_conflits.iloc[0]["conflit"],
                int(par_annee.loc[par_annee["soldats"].idxmax(), "annee_deces"]),
            ],
        }
    )

    return {
        "viz": viz,
        "resume_conflits": resume_conflits,
        "resume_departements": resume_departements,
        "par_annee": par_annee,
        "par_decennie": par_decennie,
        "prenoms": prenoms,
        "synthese": synthese,
    }