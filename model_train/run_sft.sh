accelerate launch --config_file ./accelerate_configs/deepspeed_zero3_4nodes.yaml \
  supervised_finetune.py --model_path model_path \
  --data_path example_data_for_train/sft_data.jsonl