from utils.compute_avg import *
import torch
import utils.debug

VERBOSE_SIZE = 1

def train_epoch(model, data_loader, criterion, optimizer, epoch, log_interval, device):
    model.train()
    print('Train start', end=': ')

    train_loss = 0.0
    losses = ComputeAvg()
    accuracies = ComputeAvg()
    for batch_idx, (data, targets) in enumerate(data_loader):
        data, targets = data.to(device), targets.to(device)
        outputs = model(data)
        loss = criterion(outputs, targets)
        acc = calculate_acc(outputs, targets)

        train_loss += loss.item()
        losses.update(loss.item(), data.size(0))
        accuracies.update(acc, data.size(0))

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if (batch_idx + 1) % log_interval == 0:
            avg_loss = train_loss / log_interval
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, (batch_idx + 1) * len(data), len(data_loader.dataset), 100. * (batch_idx + 1) / len(data_loader),
                avg_loss))
            train_loss = 0.0

        if (batch_idx + 1) % VERBOSE_SIZE == 0:
            utils.debug.process()


    print(f"Train Done ({len(data_loader.dataset)}"
          f" samples): Average loss: {losses.avg:.4f}\t"
          f"Acc: {(accuracies.avg*100):.4f}%")

    return losses.avg, accuracies.avg

def val_epoch(model, data_loader, criterion, device):
    model.eval()
    print(f'val start', end=': ')
    losses = ComputeAvg()
    accuracies = ComputeAvg()
    with torch.no_grad():
        for (data, targets) in data_loader:
            data, targets = data.to(device), targets.to(device)
            outputs = model(data)

            loss = criterion(outputs, targets)
            acc = calculate_acc(outputs, targets)

            losses.update(loss.item(), data.size(0))
            accuracies.update(acc, data.size(0))
            # print('epoch')
    # show info


    print(f"Validation Done ({len(data_loader.dataset)}"
          f" samples): Average loss: {losses.avg:.4f}\t"
          f"Acc: {(accuracies.avg * 100):.4f}%")

    return losses.avg, accuracies.avg