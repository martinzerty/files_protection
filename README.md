# files_protection

On peut déchiffrer des fichiers pour les lire et en chiffrer


Lancer ```open.sh``` pour déchiffrer les fichiers et ```close.sh``` pour en chiffrer.

```open.sh``` déchiffre les fichiers présents dans ```data/content```, les met dans ```data/open``` et supprime les fichiers déchiffrés à la fin de la session.

```close.sh``` chiffre les fichiers présents dans ```data/open``` pour les mettre dans ```data/content```. Cela supprime aussi les fichiers présents dans ```data/open``` à la fin.

## Clef

La clef est ```DxDh0Vv0yVGLyaVxEIke1NoiqA7i0EPig13RqMqD5jI=```

## Modules

Les programme utilise :

• ```os```

• ```hashlib```

• ```cryptography```

• ```shutil```

• ```getpass```

• ```sys```
