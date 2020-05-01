def printN(word, model):
	print(word)
	#print(model.get_nearest_neighbors(word, on_unicode_error='replace'))
	print(model.get_nearest_neighbors(word))
	print("\n\n")

import fasttext
model = fasttext.train_unsupervised(input='DC-poem-formatUTF.txt', minn=3, maxn=6, dim=100, epoch=20)


model.save_model("embeddings.bin")



printN("tanto", model)
printN("gentile", model)
printN("onesta", model)
printN("pare", model)
printN("la", model)
printN("donna", model)
printN("mia", model)
printN("altrui", model)
printN("saluta", model)
printN("")
