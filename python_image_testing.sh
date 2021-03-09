declare -a StringArray=("vgg16" "vgg19" "inception" "xception" "resnet" )

for val in ${StringArray[@]}; do
	for i in {1..11}; do 
		 python classify_image.py --model "$val" --image images/test"$i".jpg --output output_result_image/"$val"_output/"$val"_test"$i"_output.jpg
	done
done
