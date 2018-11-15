import os
import weather_class
import unittest
import tempfile
import json



class TestCase(unittest.TestCase):

    # --------------------------------------------------------------------------
    def setUp(self):
        self.city = "Madrid"
        self.temp = 40.0
        self.new_city = "Barcelona"
        self.new_temp = 30.0
        # Creo una instancia de la clase
        self.previous_id = weather_class.Prediction.ID
        self.pred = weather_class.Prediction(self.city,self.temp)

    # --------------------------------------------------------------------------
    def test_object_from_class(self):

        # Comprobamos que el objeto prediccion es de la clase Prediction
        self.assertIsInstance(self.pred, weather_class.Prediction,
        "Comprobación de que la instancia es de la clase")

        # Como existen elementos de la clase, no puede ser 0
        self.assertTrue(self.pred.ID>0,
        "Comprobación de que el objeto se ha creado y el valor de ID ha aumentado")

        pass
    # --------------------------------------------------------------------------
    def test_create_object(self):

        # Comprobamos que el parámetro city devuelve lo que tiene que devolver
        self.assertEqual(self.pred["city"],self.city,
        "Comprobación de que el atributo city se ha asignado correctamente")

        # Comprobamos que el parámetro temperatura devuelve lo correcto
        self.assertEqual(self.pred["temperature"],self.temp,
        "Comprobación de que el atributo temperature es correcto")

        # Como es el primer elemento añadido, su ID tiene que coincidir con
        # el siguiente valor de ID.
        self.assertEqual(self.pred["ID"],self.previous_id+1,
        "Comprobación de que el atributo ID es correcto")
        self.assertEqual(self.pred["ID"],weather_class.Prediction.ID,
        "Comprobación de que el atributo ID tiene el valor que le corresponde")
        actual_ID = weather_class.Prediction.ID

        # Ahora comprobamos que la asignación de ID es correcta
        # Si ahora creamos otro objeto, su id tiene que ser 2.
        self.pred2 = weather_class.Prediction(self.city,self.temp)
        self.assertEqual(self.pred2["ID"],actual_ID+1,
        "Comprobación de que el valor del ID se incrementa de forma correcta")


        #Si creamos tres objetos más, debe ser 4
        self.pred3 = weather_class.Prediction(self.city,self.temp)
        self.pred4 = weather_class.Prediction(self.city,self.temp)
        self.assertEqual(self.pred4["ID"],actual_ID+3,
        "Comprobación de que el valor del ID se incrementa de forma correcta")

        pass

    # --------------------------------------------------------------------------
    def test_modify_city(self):

        # Hacemos un cambio del valor de la ciudad
        self.pred.set_city(self.new_city)

        # Comprobamos que tras el cambio no es "Madrid",
        self.assertNotEqual(self.pred["city"],self.city,
        "Comprobación de que el valor de city se modifica de forma correcta")

        # Comprobamos que tras el cambio, es "Barcelona"
        self.assertEqual(self.pred["city"],self.new_city,
        "Comprobación de que el valor de city se modifica al correcto")

        # Me aseguro
        self.assertEqual(self.pred["city"],"Barcelona",
        "Comprobación de que el valor de city es el que queremos")
        pass

    # --------------------------------------------------------------------------
    def test_modify_temperature(self):

        # Hacemos un cambio del valor de la ciudad
        self.pred.set_temperature(self.new_temp)

        # Comprobamos que tras el cambio no es "Madrid",
        self.assertNotEqual(self.pred["temperature"],self.temp,
        "Comprobación de que el valor de city se modifica de forma correcta")

        # Comprobamos que tras el cambio, es "Barcelona"
        self.assertEqual(self.pred["temperature"],self.new_temp,
        "Comprobación de que el valor de city se modifica al correcto")

        # Me aseguro
        self.assertEqual(self.pred["temperature"],30.0,
        "Comprobación de que el valor de city es el que queremos")

        # https://stackoverflow.com/questions/129507/how-do-you-test-that-a-python-function-throws-an-exception
        # self.assertRaises("AssertionError", self.pred.set_temperature)
        pass

    # --------------------------------------------------------------------------
    def test_types(self):
        # Compruebo que la temperatura es un número
        self.assertTrue(type(self.pred.temperature) == float or
        type(self.pred.temperature) == int,
        "Comprobación de que el atributo temperature es del tipo correcto")

        # Compruebo que la ciudad es un string
        self.assertIsInstance(self.pred.city, str,
        "Comprobación de que el atributo ciudad es del tipo correcto")

        # Compruebo que el tipo ID es un entero
        self.assertIsInstance(self.pred.ID, int,
        "Comprobación de que el atributo ID es del tipo correcto")
        self.assertTrue(self.pred.ID > 0,
        "Comprobación de que el atributo ID mayor que cero")

        self.assertIsInstance(self.pred.date, str,
        "Comprobación de que el atributo fecha es del tipo correcto")
        pass

    # --------------------------------------------------------------------------
    def test_len_object(self):
        # El tamaño de la clase tiene que ser 4, porque tiene 4 atributos.
        self.assertEqual(len(self.pred),4,
        "Comprobación de que hay 4 atributos")
        pass

    # --------------------------------------------------------------------------
    def test_date_format(self):

        # Comprobamos que la fecha está en un formato correcto: los separadores
        # en las posiciones correctas, y el resto de valores son números

        self.assertTrue(self.pred.date[2]=='-' and self.pred.date [5]=='-',
        "Comprobación de que el atributo date tiene el formato correcto")

        for i,elem in enumerate(self.pred.date):
            if i is not 2 and i is not 5:
                self.assertTrue(0<=int(elem)<=9,
                "Comprobación de que el atributo date tiene el formato correcto")
        pass


if __name__ == "__main__" :
    unittest.main()
