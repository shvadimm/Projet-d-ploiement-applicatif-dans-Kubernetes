#!/usr/bin/env python3
"""Script pour ajouter les colonnes priority et due_date à la table todos."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from app import create_app
from app.extensions import db

def migrate():
    app = create_app()
    with app.app_context():
        # Utilise raw SQL pour ajouter les colonnes (MySQL)
        try:
            db.session.execute(text("ALTER TABLE todos ADD COLUMN priority VARCHAR(20) DEFAULT 'medium'"))
            db.session.commit()
            print("Colonne 'priority' ajoutée.")
        except Exception as e:
            if "Duplicate column" in str(e) or "1060" in str(e):
                print("Colonne 'priority' existe déjà.")
            else:
                db.session.rollback()
                print(f"Erreur priority: {e}")
        try:
            db.session.execute(text("ALTER TABLE todos ADD COLUMN due_date DATE"))
            db.session.commit()
            print("Colonne 'due_date' ajoutée.")
        except Exception as e:
            if "Duplicate column" in str(e) or "1060" in str(e):
                print("Colonne 'due_date' existe déjà.")
            else:
                db.session.rollback()
                print(f"Erreur due_date: {e}")

if __name__ == "__main__":
    migrate()
