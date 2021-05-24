# commande à taper en ligne de commande après la sauvegarde de ce fichier:
# python setup.py build
from cx_Freeze import setup, Executable

executables = [
    Executable(script="main.py",  base="Win32GUI")
]
'''icon="nom_de_l_icone.ico",'''
# ne pas mettre "base = ..." si le programme n'est pas en mode graphique, comme c'est le cas pour chiffrement.py.

buildOptions = dict(
    includes=["Game"],
    include_files=["datas/game_init.gin"]
)

setup(
    name="SokoGap",
    version="1.0",
    description="Jeu developper dans le cadre du cours Programmation 2D",
    author="La Classe GAP de Polytechnique Yaoundé",
    options=dict(build_exe=buildOptions),
    executables=executables
)