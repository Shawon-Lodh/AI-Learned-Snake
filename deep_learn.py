from sklearn.model_selection import train_test_split
import json
import torch
import torch.nn as nn


def find_predicted_value(running_model, dataset_x):
    value = 0
    dataset_x = torch.tensor(dataset_x)
    dataset_pred = running_model(dataset_x.float())
    if dataset_pred.float() > 0.5:
        value = 1
    elif dataset_pred.float() < -0.5:
        value = -1
    else:
        value = 0
    return value


def accuracy(running_model, dataset_x, dataset_y):
    dataset_pred = running_model(dataset_x.float())
    accuracte_dataset_pred = []
    for i in dataset_pred:
        if i.float() > 0.5:
            accuracte_dataset_pred.append(1)
        elif i.float() < -0.5:
            accuracte_dataset_pred.append(-1)
        else:
            accuracte_dataset_pred.append(0)

    accuracte_dataset_pred = torch.tensor(accuracte_dataset_pred)

    total_dataset = dataset_x.size(0)
    correct_dataset = accuracte_dataset_pred.eq(dataset_y.data).sum().item()
    dataset_accuracy = 100 * correct_dataset / total_dataset

    return dataset_accuracy


def training(running_model, lrn_rate, epoch,train_x,train_y):
    # Construct the loss function
    # criterion = nn.BCELoss()  ###Binary cross entropy loss
    criterion = nn.MSELoss()
    # Construct the optimizer (Stochastic Gradient Descent in this case)
    optimizer = torch.optim.Adam(running_model.parameters(), lr=lrn_rate)

    # Gradient Descent
    for e in range(epoch):
        # Forward pass: Compute predicted y by passing x to the model
        train_pred = running_model(train_x.float())

        # print(train_pred.type())

        # Compute and print loss
        loss = criterion(train_pred, train_y.unsqueeze(1).float())

        # Zero gradients, perform a backward pass, and update the weights.
        optimizer.zero_grad()

        # perform a backward pass (backpropagation)
        loss.backward()

        # Update the parameters
        optimizer.step()

        # compute accuracy
        train_accuracy = accuracy(running_model, train_x, train_y)

        print('epoch: ', e, ' loss: ', loss.item(), ' accuracy: ', train_accuracy)



def main_model():
    f = open("train_x_data.json")
    train_x_data = json.load(f)

    f1 = open("train_y_data.json")
    train_y_data = json.load(f1)

    # train_x_data, test_x_data, train_y_data, test_y_data = train_test_split(d, d1, test_size=0.5, random_state=0)

    # # print('\n',train_x_data,'\n\n',test_x_data)

    train_x = torch.tensor(train_x_data)
    train_y = torch.tensor(train_y_data)
    # test_x = torch.tensor(test_x_data)
    # test_y = torch.tensor(test_y_data)

    input = (train_x.size()[1])  # dimention
    hidden1 = 25
    hidden2 = 10
    output = 1
    #
    # # Create a model
    model = nn.Sequential(nn.Linear(input, hidden1),
                          nn.ReLU(),
                          nn.Linear(hidden1, hidden2),
                          nn.ReLU(),
                          nn.Linear(hidden2, output),
                          nn.Tanh()
                          )
    training(model, 0.1, 100,train_x,train_y)
    # return model
    return model,train_x,train_y
# # torch.save(model, 'D:\Education\4.2\pygame_and_others\snake\trained_model1.pth')
# train_accuracy = accuracy(model, train_x, train_y)
# test_accuracy = accuracy(model, test_x, test_y)
# print("Train Accuracy : ", train_accuracy, " Test Accuracy : ", test_accuracy)
# print(find_predicted_value(model, [0, 0, 0, -0.5, -1]))

model,train_x,train_y = main_model()
# model = torch.load(r'model1.pth')
train_accuracy = accuracy(model, train_x, train_y)
# test_accuracy = accuracy(model, test_x, test_y)
print("Train Accuracy : ", train_accuracy)
print(find_predicted_value(model, [0, 0, 0, -0.5, -1]))


