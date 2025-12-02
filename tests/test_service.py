import pytest
import jwt
from datetime import datetime, timedelta, timezone
from unittest.mock import Mock, patch
from src.service import UniversityAdmissionService, InputModel
from src.jwt_middleware import create_jwt_token, JWT_SECRET_KEY, JWT_ALGORITHM, USERS


class TestJWTAuthentication:
    '''Test suite for JWT authentication functionality'''
    
    def test_valid_jwt_token_creation(self):
        '''Verify that a valid JWT token is created for a user'''
        user_id = 'user123'
        token = create_jwt_token(user_id)
        
        # Decode token to verify it's valid
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        
        assert payload['sub'] == user_id
        assert 'exp' in payload
        assert payload['exp'] > datetime.now(timezone.utc).timestamp()
    
    def test_jwt_token_expiration(self):
        '''Verify that authentication fails if the JWT token has expired'''
        user_id = 'user123'
        
        # Create an expired token
        expiration = datetime.now(timezone.utc) - timedelta(hours=1)
        payload = {'sub': user_id, 'exp': expiration.timestamp()}
        expired_token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        
        # Verify token has expired
        with pytest.raises(jwt.ExpiredSignatureError):
            jwt.decode(expired_token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    
    def test_invalid_jwt_token(self):
        '''Verify that authentication fails if the JWT token is invalid'''
        invalid_token = 'invalid.token.here'
        
        # Verify invalid token raises exception
        with pytest.raises(jwt.InvalidTokenError):
            jwt.decode(invalid_token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    
    def test_jwt_token_with_wrong_secret(self):
        '''Verify that authentication fails if the JWT token was signed with wrong secret'''
        user_id = 'user123'
        wrong_secret = 'wrong_secret_key'
        
        # Create token with wrong secret
        expiration = datetime.now(timezone.utc) + timedelta(hours=1)
        payload = {'sub': user_id, 'exp': expiration.timestamp()}
        token = jwt.encode(payload, wrong_secret, algorithm=JWT_ALGORITHM)
        
        # Verify token fails validation
        with pytest.raises(jwt.InvalidTokenError):
            jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])


class TestLoginAPI:
    '''Test suite for login API functionality'''
    
    @patch('src.service.bentoml.models.get')
    def test_login_with_valid_credentials(self, mock_model_get):
        '''Verify that the API returns a valid JWT token for correct user credentials'''
        # Mock the model loading
        mock_model_get.return_value.load_model.return_value = Mock()
        
        # Create service instance
        service = UniversityAdmissionService()
        
        # Test valid credentials
        credentials = {
            'username': 'user123',
            'password': 'password123'
        }
        
        result = service.login(credentials)
        
        # Verify token is returned
        assert 'token' in result
        assert result['token'] is not None
        
        # Verify token is valid
        token = result['token']
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        assert payload['sub'] == 'user123'
    
    @patch('src.service.bentoml.models.get')
    def test_login_with_invalid_username(self, mock_model_get):
        '''Verify that the API returns a 401 error for incorrect username'''
        # Mock the model loading
        mock_model_get.return_value.load_model.return_value = Mock()
        
        # Create service instance
        service = UniversityAdmissionService()
        
        # Test invalid username
        credentials = {
            'username': 'invalid_user',
            'password': 'password123'
        }
        
        result = service.login(credentials)
        
        # Verify 401 response
        assert hasattr(result, 'status_code')
        assert result.status_code == 401
    
    @patch('src.service.bentoml.models.get')
    def test_login_with_invalid_password(self, mock_model_get):
        '''Verify that the API returns a 401 error for incorrect password'''
        # Mock the model loading
        mock_model_get.return_value.load_model.return_value = Mock()
        
        # Create service instance
        service = UniversityAdmissionService()
        
        # Test invalid password
        credentials = {
            'username': 'user123',
            'password': 'wrong_password'
        }
        
        result = service.login(credentials)
        
        # Verify 401 response
        assert hasattr(result, 'status_code')
        assert result.status_code == 401
    
    @patch('src.service.bentoml.models.get')
    def test_login_with_missing_username(self, mock_model_get):
        '''Verify that the API returns a 401 error for missing username'''
        # Mock the model loading
        mock_model_get.return_value.load_model.return_value = Mock()
        
        # Create service instance
        service = UniversityAdmissionService()
        
        # Test missing username
        credentials = {
            'password': 'password123'
        }
        
        result = service.login(credentials)
        
        # Verify 401 response
        assert hasattr(result, 'status_code')
        assert result.status_code == 401
    
    @patch('src.service.bentoml.models.get')
    def test_login_with_missing_password(self, mock_model_get):
        '''Verify that the API returns a 401 error for missing password'''
        # Mock the model loading
        mock_model_get.return_value.load_model.return_value = Mock()
        
        # Create service instance
        service = UniversityAdmissionService()
        
        # Test missing password
        credentials = {
            'username': 'user123'
        }
        
        result = service.login(credentials)
        
        # Verify 401 response
        assert hasattr(result, 'status_code')
        assert result.status_code == 401


class TestPredictionAPI:
    '''Test suite for prediction API functionality'''
    
    @patch('src.service.bentoml.models.get')
    def test_predict_with_valid_input(self, mock_model_get):
        '''Verify that the API returns a valid prediction for correct input data'''
        # Mock the model
        mock_model = Mock()
        mock_model.predict.return_value = [0.85]
        mock_model_get.return_value.load_model.return_value = mock_model
        
        # Create service instance
        service = UniversityAdmissionService()
        
        # Create valid input data
        input_data = InputModel(
            gre_score=320,
            toefl_score=110,
            university_rating=4,
            sop=4.5,
            lor=4.0,
            cgpa=9.0,
            research=1
        )
        
        result = service.predict(input_data)
        
        # Verify prediction is returned
        assert 'admission_chance' in result
        assert isinstance(result['admission_chance'], float)
        assert result['admission_chance'] == 0.85
    
    @patch('src.service.bentoml.models.get')
    def test_predict_with_minimum_values(self, mock_model_get):
        '''Verify that the API handles minimum valid input values'''
        # Mock the model
        mock_model = Mock()
        mock_model.predict.return_value = [0.15]
        mock_model_get.return_value.load_model.return_value = mock_model
        
        # Create service instance
        service = UniversityAdmissionService()
        
        # Create input with minimum values
        input_data = InputModel(
            gre_score=260,
            toefl_score=80,
            university_rating=1,
            sop=1.0,
            lor=1.0,
            cgpa=6.0,
            research=0
        )
        
        result = service.predict(input_data)
        
        # Verify prediction is returned
        assert 'admission_chance' in result
        assert isinstance(result['admission_chance'], float)
    
    @patch('src.service.bentoml.models.get')
    def test_predict_with_maximum_values(self, mock_model_get):
        '''Verify that the API handles maximum valid input values'''
        # Mock the model
        mock_model = Mock()
        mock_model.predict.return_value = [0.95]
        mock_model_get.return_value.load_model.return_value = mock_model
        
        # Create service instance
        service = UniversityAdmissionService()
        
        # Create input with maximum values
        input_data = InputModel(
            gre_score=340,
            toefl_score=120,
            university_rating=5,
            sop=5.0,
            lor=5.0,
            cgpa=10.0,
            research=1
        )
        
        result = service.predict(input_data)
        
        # Verify prediction is returned
        assert 'admission_chance' in result
        assert isinstance(result['admission_chance'], float)
    
    def test_invalid_input_missing_required_field(self):
        '''Verify that the API returns an error for invalid input data with missing field'''
        # Test missing required field - should raise validation error
        with pytest.raises(Exception):
            InputModel(
                gre_score=320,
                toefl_score=110,
                university_rating=4,
                sop=4.5,
                lor=4.0,
                cgpa=9.0
                # Missing research field
            )
    
    def test_invalid_input_wrong_data_type(self):
        '''Verify that the API returns an error for invalid input data with wrong type'''
        # Test wrong data type - should raise validation error
        with pytest.raises(Exception):
            InputModel(
                gre_score='not_a_number',  # Should be int
                toefl_score=110,
                university_rating=4,
                sop=4.5,
                lor=4.0,
                cgpa=9.0,
                research=1
            )
    
    @patch('src.service.bentoml.models.get')
    def test_predict_dataframe_column_names(self, mock_model_get):
        '''Verify that the DataFrame passed to model has correct column names'''
        # Mock the model
        mock_model = Mock()
        mock_model.predict.return_value = [0.85]
        mock_model_get.return_value.load_model.return_value = mock_model
        
        # Create service instance
        service = UniversityAdmissionService()
        
        # Create valid input data
        input_data = InputModel(
            gre_score=320,
            toefl_score=110,
            university_rating=4,
            sop=4.5,
            lor=4.0,
            cgpa=9.0,
            research=1
        )
        
        service.predict(input_data)
        
        # Verify predict was called
        assert mock_model.predict.called
        
        # Get the DataFrame that was passed to predict
        call_args = mock_model.predict.call_args[0][0]
        
        # Verify column names match training data format
        expected_columns = ['GRE Score', 'TOEFL Score', 'University Rating', 'SOP', 'LOR ', 'CGPA', 'Research']
        assert list(call_args.columns) == expected_columns


class TestInputModelValidation:
    '''Test suite for InputModel validation'''
    
    def test_valid_input_model(self):
        '''Verify that InputModel accepts valid data'''
        input_data = InputModel(
            gre_score=320,
            toefl_score=110,
            university_rating=4,
            sop=4.5,
            lor=4.0,
            cgpa=9.0,
            research=1
        )
        
        assert input_data.gre_score == 320
        assert input_data.toefl_score == 110
        assert input_data.university_rating == 4
        assert input_data.sop == 4.5
        assert input_data.lor == 4.0
        assert input_data.cgpa == 9.0
        assert input_data.research == 1
