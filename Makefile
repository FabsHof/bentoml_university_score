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