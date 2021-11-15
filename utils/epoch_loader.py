from utils.compute_avg import *
import torch
import utils.debug
from tqdm import tqdm

# this is old version of frame work, check new version in worker.train

VERBOSE_SIZE = 1

def train_epoch(model, data_loader, criterion, optimizer, epoch, log_interval, device):
    model.train()

    train_loss = 0.0
    losses = ComputeAvg()
    accuracies = ComputeAvg()
    batch_idx = 0

    for (data, targets) in tqdm(data_loader, desc='Train ::'):
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
            print(f' log e[{epoch}]: [{(batch_idx + 1) * len(data)}/{len(data_loader.dataset)} ({((batch_idx + 1)/len(data_loader))*100.0:.0f}%)]\tLoss: {avg_loss:.6f}'
                )
            train_loss = 0.0

        batch_idx += 1


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
        for (data, targets) in tqdm(data_loader, desc='val epoch:: '):
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