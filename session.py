import json
import matplotlib.pyplot as plt

def reading_data():
    sessions = []
    with open("sessions.jsonl") as f:
        for line in f:
            line = line.strip()
            if line:
                sessions.append(json.loads(line))
    return sessions

def counter(sessions):
    d = dict()
    for arr in sessions:
        for item in arr:
            d[item] = d.get(item,0) + 1
    return d

def session_lenght(sessions):
    lenghts = [len(i) for i in sessions]
    return lenghts

def unique_share(session):
    shares = [round(len(set(i))/len(i),2) for i in session]
    return shares

def display_tops(data):
    size = len(data)
    print("Лучшие показатели:")
    for i in range(size):
        print(f"{i + 1}. id: {data[i][0]} count: {data[i][1]}")

def show_statistic(sessions):
    print(f"Общее количество сессий: {len(sessions)}")
    lenghts = session_lenght(sessions)
    avg_lenght = sum(lenghts)/len(lenghts)
    cnt_lenght = len([l for l in lenghts if l > avg_lenght])
    print(f"Максимальная длина сессии: {max(lenghts)}")
    print(f"Минимальная длина сессии: {min(lenghts)}")
    print(f"Средняя длина сессий: {avg_lenght:.2f}")
    print(f"Количество сессий с длиной больше средней: {cnt_lenght}")
    item = counter(sessions)
    print(f"Количество уникальных товаров: {len(item)}")
    popular_item = tuple(sorted(item.items(), key=lambda i: i[1], reverse=True))[:10]
    display_tops(popular_item)
    shares = unique_share(sessions)
    avg_shares = sum(shares)/len(shares)
    print(f"Максимальная доля уникальных товаров в сессии: {max(shares)}")
    print(f"Минимальная доля уникальных товаров в сессии: {min(shares)}")
    print(f"Средняя доля униальных товаров: {avg_shares:.2f}")
    plt.figure(figsize=[8, 4])
    plt.hist(lenghts, bins=10)
    plt.title("Длины сессий")
    plt.xlabel("Длина сессии")
    plt.ylabel("Кол-во сессий")
    plt.savefig("lenghts.png")
    plt.figure(figsize=[8,4])
    plt.hist(shares, bins=10)
    plt.title("Доли уникальных товаров в сессии")
    plt.xlabel("Доля уникальных товаров в сессии")
    plt.ylabel("Кол-во уникальных товаров")
    plt.savefig("shares.png")
    plt.figure(figsize=[8,4])
    plt.hist(item.values(), bins=20)
    plt.title("Частоты просмотров товаров")
    plt.xlabel("Частота товаров")
    plt.ylabel("Кол-во товаров")
    plt.savefig("frequences.png")

def train_test_split(session):
    train_session = []
    test_target = []
    for i in session:
        train_session.append(i[:-1])
        test_target.append(i[-1])
    return train_session, test_target

def convert_to_top10(data):
    size = len(data)
    top10 = list()
    for i in range(size):
        top10.append(data[i][0])
    return top10

def create_graph(train_session):
    graph = {}
    for i in train_session:
        for j in range(len(i) - 1):
            if i[j] not in graph:
                graph[i[j]] = {}
            graph[i[j]][i[j+1]] = graph[i[j]].get(i[j + 1], 0) + 1
    return graph


def convert_to_probability(graph):
    for curr, next_ids in graph.items():
        curr_sum = sum(next_ids.values())
        for next_id in next_ids:
            graph[curr][next_id] = round(next_ids[next_id] / curr_sum, 4)
    return graph

def recommended_model(train_session, top10, graph):
    all_recommended = []
    size = len(train_session)
    for i in range(size):
        curr_item = train_session[i][-1]
        sort_arr = list(sorted(graph.get(curr_item, {}).items(), key=lambda i: i[1], reverse=True))
        recommend = [i for i, _ in sort_arr]
        ind = 0
        if len(recommend) < 10:
            while len(recommend) != 10:
                if top10[ind] in recommend:
                    ind += 1
                else:
                    recommend.append(top10[ind])
                    ind += 1
        all_recommended.append(recommend)
    return all_recommended

def hit_test(recommend, test_target):
    size = len(test_target)
    hit = 0
    for i in range(size):
        if test_target[i] in recommend[i]:
            hit += 1
    return hit / size

def main():
    sessions = reading_data()
    show_statistic(sessions)
    item = counter(sessions)
    popular_item = list(sorted(item.items(), key=lambda i: i[1], reverse=True))[:10]
    top10 = convert_to_top10(popular_item)
    train_sessions, test_targets = train_test_split(sessions)
    graph_p = create_graph(train_sessions)
    probabilities = convert_to_probability(graph_p)
    all_recommended = recommended_model(train_sessions, top10, probabilities)
    my_recommended_model = hit_test(all_recommended, test_targets)
    baseline_arr = [top10] * len(test_targets)
    baseline_recommended_model = hit_test(baseline_arr, test_targets)
    print(f"Результаты теста hit@10 для моей модели: {my_recommended_model:.3f}")
    print(f"Результаты теста hit@10 для топ10 товаров: {baseline_recommended_model:.3f}")

if __name__ == "__main__":
    main()
