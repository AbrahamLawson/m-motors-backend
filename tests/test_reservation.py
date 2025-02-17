import sys
import os
import unittest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.user import User
from app.models.vehicule import Vehicule
from app.models.reservation import Reservation
from app.database import Base


# Object de notre test : Attribuer un nom au dossier de réservation

# Configuration de la bdd en mémoire pour les tests
engine = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=engine)

class ReservationTest(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(engine)
        self.session = Session(bind=engine)

    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(engine)

    def test_reservation_repertory_name_generation(self):
        # Création d'un user et d'un vehicule tests
        user = User(civility="Mr", first_name="John", last_name="Doe", 
                    email="john.doe@example.com", phone_number="123-456-7890", 
                    address="123 Main St", zip_code="12345", role="user", 
                    password="password")
        vehicule = Vehicule(model="Model S", color="Red", picture="path/to/picture.jpg",
                           year=2020, kilometers=10000, location_price=100, 
                           sell_price=50000, description="A nice car", 
                           disponibilities=True)
        self.session.add(user)
        self.session.add(vehicule)
        self.session.commit()

        # Création d'une réservation avec tous les champs
        start_date = datetime.now()
        end_date = datetime.now()
        reservation = Reservation(user=user, user_id=user.id, 
                                vehicule_id=vehicule.id, 
                                start_date=start_date, 
                                end_date=end_date)
        self.session.add(reservation)
        self.session.commit()

        # Vérif si le nom du répertoire est bien généré
        expected_repertory_name = f"{start_date.strftime('%Y%m%d')}_{user.first_name}-{user.last_name}_{vehicule.id}"
        print(f"\nNom de répertoire attendu: {expected_repertory_name}")
        print(f"Nom de répertoire généré: {reservation.repertory_name}")
        self.assertEqual(reservation.repertory_name, expected_repertory_name)

    def test_reservation_repertory_name_default_value(self):
        # Création d'une réservation avec des champs manquants (pour éviter les bugs)
        user = User(civility="Mr", first_name="Jane", last_name="Smith", 
                    email="jane.smith@example.com", phone_number="987-654-3210", 
                    address="456 Elm St", zip_code="67890", role="user", 
                    password="password")
        vehicule = Vehicule(model="Model X", color="Blue", picture="path/to/picture2.jpg",
                           year=2022, kilometers=5000, location_price=150, 
                           sell_price=75000, description="Another nice car", 
                           disponibilities=True)
        self.session.add(user)
        self.session.add(vehicule)
        self.session.commit()
    
        # Création d'une réservation avec la valeur default
        reservation = Reservation(user_id=user.id, vehicule_id=vehicule.id,
                                start_date=datetime.now(), end_date=datetime.now())
        self.session.add(reservation)
        self.session.commit()

        # Vérif du nom du répertoire à la valeur default
        print(f"Nom de répertoire généré: {reservation.repertory_name}")
        self.assertEqual(reservation.repertory_name, "default_repertory_name")

if __name__ == '__main__':
    unittest.main()