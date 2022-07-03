from utils import story

# lst, cnt = story.count_all('./story')

# target = story.find_str('./story/main/8_怒号光明', 'Video')

count = story.sum_words_in_dir('./story/activities/尘影余音')
# count = story.sum_words_in_dir('./story/main/10_破碎日冕')
count_memory = story.sum_words_in_dir('./story/memory/new')
# count = story.count_words_in_file('./story/memory/memory/story_12fce_1_1.txt')
print(count)
print(count_memory)
