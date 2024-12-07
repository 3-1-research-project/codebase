using Microsoft.EntityFrameworkCore;
using Minitwit.Core.Entities;
using Minitwit.Core.Repository;

namespace Minitwit.Infrastructure.Repository;

public class MessageRepository : BaseRepository, IMessageRepository
{
    public MessageRepository(MinitwitDbContext DbContext)
        : base(DbContext) { }

    public async Task<ICollection<Message>> GetMessagesByPageAsync(int page)
    {
        //Use EF to get the specified page of Messages from the database
        ICollection<Message> Messages = await db
            .Messages.OrderByDescending(c => c.TimeStamp)
            .Skip(PageSize * (page - 1))
            .Take(PageSize)
            .ToListAsync();

        return Messages;
    }

    public async Task<ICollection<Message>> GetMessagesByCountAsync(int count)
    {
        ICollection<Message> Messages = await db
            .Messages.OrderByDescending(c => c.TimeStamp)
            .Take(count)
            .AsNoTracking()
            .ToListAsync();

        return Messages;
    }

    public async Task<ICollection<Message>> GetMessagesFromAuthorByCountAsync(int authorId, int count)
    {
        //Use EF to get the specified count of Messages from an author from the database
        ICollection<Message> Messages = await db
            .Messages.Where(c => c.AuthorId == authorId)
            .OrderByDescending(c => c.TimeStamp)
            .Take(count)
            .ToListAsync();

        return Messages;
    }

    public async Task<int> GetMessageCountAsync()
    {
        //U se EF to get the total number of Messages from the database
        return await db.Messages.CountAsync();
    }

    public async Task<int> GetPageCountAsync()
    {
        return await GetMessageCountAsync() / PageSize + 1;
    }

    public async Task AddMessageAsync(Message messageDto)
    {
        await db.Messages.AddAsync(messageDto);
        await db.SaveChangesAsync();
    }

    public async Task<Message> AddCreateMessageAsync(CreateMessage message)
    {
        Message entity = new Message()
        {
            MessageId = new int(),
            Text = message.Text,
            TimeStamp = DateTime.Now,
            AuthorId = message.AuthorId
        };

        await AddMessageAsync(entity);

        return entity;
    }
}
