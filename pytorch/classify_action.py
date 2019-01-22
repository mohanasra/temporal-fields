import operator
import csv

def load_epoch_result(epoch_result_file):
    epoch_data = {}
    with open(epoch_result_file) as epoch_results:
        for line in epoch_results:
            epoch_data = {}
            values = line.split(" ")
            id = values[0]
            values = values[1:]
            looping = 0
            for entry in values:
                epoch_data[looping] = float(values[looping]) 
                looping += 1
#             key_max = max(epoch_data.keys(), key=(lambda k: epoch_data[k]))
#             top5 = dict(sorted(epoch_data.iteritems(), key=operator.itemgetter(1), reverse=True)[:5])
            top5 = sorted(epoch_data.iteritems(), key=operator.itemgetter(1), reverse=True)[:5]
#             top5 = sorted(top5.iteritems(), key=operator.itemgetter(1), reverse=True) 
#             print('id - {}, top5 - {}'.format(id, top5))
        return top5

def epoch_result(epoch_result_file, charades_classes, test_data, print_logs=False):
    video_scores = {}
    score_range = [0.31, 0.95]
    MIN_IDX = 0
    MAX_IDX = 1
    SCORE_UPPER_LIMIT = 0.8
    with open(epoch_result_file) as epoch_results:
        for line in epoch_results:
            epoch_data = {}
            values = line.split(" ")
            id = values[0]
            if(print_logs):
                print("Duration of {} is {}...\n".format(id, test_data[id]['duration']))
            values = values[1:]
            looping = 0
            actions = ""
            score = 0.0
            weight = 1.0

            for entry in values:
                epoch_data[looping] = float(values[looping]) 
                looping += 1
            top5 = sorted(epoch_data.iteritems(), key=operator.itemgetter(1), reverse=True)[:5]
            if(print_logs):
                print("top5 = {}".format(top5))
            for classification_result in top5:
                actions += "\t{}\n".format(charades_classes[classification_result[0]])
                score += weight * charades_classes[classification_result[0]][1]
                weight *= weight
            score /= 5.0
#             score = 0.40
#             score = ((score - score_range[MIN_IDX])/(score_range[MAX_IDX] - score_range[MIN_IDX])) #* SCORE_UPPER_LIMIT
#             if(print_logs):
#                 print('Norm. Score - {}'.format(score))
            score = int(score*100)
            
            if(print_logs):
                print("\nFollowing are top 5 actions identified in video with id {} & score {}...\n".format(id, score))
                print(actions)
            video_scores[id] = score
        return(video_scores)


def load_charades_classes(charades_classes_file):
    charades_classes = {}
    with open(charades_classes_file) as input_file:
        for line in input_file:
            charades_class_tuple = line.split(";")
            charades_classes[int(charades_class_tuple[0])] = charades_class_tuple[1]
            
        return charades_classes
    return None

def load_charades_music_score(charades_classes_file):
    charades_score = {}
    with open(charades_classes_file) as input_file:
        for line in input_file:
            charades_class_tuple = line.split(";")
            charades_score[int(charades_class_tuple[0])] = [charades_class_tuple[1], float(charades_class_tuple[2])]
            
        return charades_score
    return None

def get_music_seed(epoch_result_file, charades_classes, test_data):
    return epoch_result(epoch_result_file, charades_classes, test_data) #, True)

def load_data_set_csv(filename):
    labels = {}
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            vid = row['id']
            actions = row['actions']
            duration = row['length']
            if actions == '':
                actions = []
            else:
                actions = [a.split(' ') for a in actions.split(';')]
                actions = [{'class': x, 'start': float(
                    y), 'end': float(z)} for x, y, z in actions]
            labels[vid] = {'actions':actions, 'duration':float(duration)}
    return labels
        
def main():
    charades_classes = load_charades_music_score('datasets/Charades_v1_classes_new.txt')
    test_data = load_data_set_csv("datasets/Charades_v1_test_small.csv")
    print("test_data {}".format(test_data))
#     print("charades classes - {}".format(charades_classes))
    seed_notes = get_music_seed('cache/asynctf_rgb_test/epoch_000.txt', charades_classes, test_data)
    max_score = max(charades_classes.values(), key = lambda item:item[1])
    min_score = min(charades_classes.values(), key = lambda item:item[1])
    possible_score_range = [max_score*5, min_score*5]
    print('max_score - {}, min_score - {}'.format(max_score, min_score))
    print('seed_notes - {}'.format(seed_notes))


if __name__ == '__main__':
    main()
