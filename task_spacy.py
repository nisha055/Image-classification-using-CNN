import spacy


nlp = spacy.load("en_core_web_sm")
# doc = nlp("Apple is looking at buying U.K. startup for $1 billion")
# print("Pipeline:", nlp.pipe_names)

# for ent in doc.ents:
# print(ent.text, ent.start_char, ent.end_char, ent.label_)

# print('---------------------------------------')
# doc_2 = nlp(u"Don't be afraid to give up the good to go for the great")

# Counting the frequencies of different POS tags:
# POS_counts = doc_2.count_by(spacy.attrs.POS)
# print(POS_counts)


def performPOS(str):
    doc = nlp(str)
    docObj = []
    for token in doc:
        temp = {}
        temp['text'] = token.text
        temp['lemma_'] = token.lemma_
        temp['pos_'] = token.pos_
        temp['tag_'] = token.tag_
        temp['dep_'] = token.dep_
        temp['shape_'] = token.shape_
        temp['is_alpha'] = token.is_alpha
        temp['is_stop'] = token.is_stop
        temp['morph'] = token.morph.get("Number")
        docObj.append(temp)
    return docObj


def ner(str):
    doc = nlp(str)
    docObj = []
    for ent in doc.ents:
        temp = {}
        temp['Text'] = ent.text
        temp['Start char'] = ent.start_char
        temp['End char'] = ent.end_char
        temp['Label'] = ent.label_
        docObj.append(temp)
    return docObj
