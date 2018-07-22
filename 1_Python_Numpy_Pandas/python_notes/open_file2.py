sentences = []
with open("some_file.txt") as f:
#    print(sentence.readline())
#    print(sentence.readline())
#    print(sentence.readline())
#    print(sentence.readline())
#    print(sentence.readline())

    for line in f:
        sentences.append(line.strip())
    
    
print(sentences)    
