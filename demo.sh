#Create conda environment
conda env create -f conda_environment.yaml
conda activate autostreaming

#Activate voicevox
cd voicevox_engine
docker-compose up -d

#Run demo
cd ..
python ./app/demo_gradio.py