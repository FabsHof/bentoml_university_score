load_data:
	@echo "⏳ Downloading and preparing data..."
	@python src/data/prepare_data.py
	@echo "✅ Data preparation complete."
prepare_data:
	@echo "⏳ Preparing data..."
	@python src/data/prepare_data.py
	@echo "✅ Data preparation complete."
train_model:
	@echo "⏳ Training model..."
	@python src/model/train_model.py
	@echo "✅ Model training complete."
start_api:
	@echo "⏳ Starting BentoML API server..."
	@bentoml serve src.service:UniversityAdmissionService
	@echo "✅ BentoML API server started."
test:
	@echo "⏳ Running unit tests..."
	@pytest tests/ -v
	@echo "✅ Tests complete."