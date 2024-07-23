#Create conda environment
conda env create -f conda_environment.yaml

#Activate voicevox
cd voicevox_engine
docker-compose up -d

#Run demo
cd ..
python ./app/main.py