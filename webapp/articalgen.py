import math
import random


def artical(select,length):
    if select == 1:
        content = "How to Stay Focused in a World Full of Distractions. Focus is becoming one of the most valuable skills in the modern world. With constant notifications, open tabs, and endless scrolling, it is harder than ever to pay attention to one thing for a long period of time. The average person is pulled in multiple directions each day, which makes deep work almost impossible. To regain your focus, you must first control your environment. Start by turning off unnecessary notifications, close extra browser tabs, and put your phone out of reach. These small actions make a big difference. Next, try working in time blocks. For example, you might work for twenty five minutes, then take a five minute break. This method trains your brain to stay on task for short periods without feeling overwhelmed. Also, remove clutter from your workspace. A clean and simple space helps reduce mental friction. Your mind mirrors your surroundings. Another key is to set clear goals before you start. Know exactly what you want to accomplish in each session. Vague goals lead to vague results. Lastly, train your focus like a muscle. Start small and gradually increase your time on focused work. Over time, your ability to concentrate will grow stronger. In a world full of noise, the ability to focus is not just useful, it is powerful. Master it and you will separate yourself from the crowd."
        parts = (content).split(" ")
    else:
        content = "The Hidden Power of Habits That Shape Your Life|10 Surprising Ways to Boost Your Creativity Today|Why Most People Fail at Budgeting—and How You Can Succeed|The Science Behind Why We Procrastinate|How to Build Unshakable Confidence in 30 Days|What Successful People Do Before Breakfast|The Truth About Digital Detox and Mental Clarity|How Minimalism Transformed My Life And Can Change Yours|5 Life Lessons Youll Wish You Learned Sooner|Why Emotional Intelligence Matters More Than IQ|How to Stay Focused in a Distracted World|The Ultimate Guide to Remote Work Productivity|What Happens to Your Brain When You Stop Multitasking|Why Morning Routines Are the Key to Success|How to Set Goals That Actually Stick|The Real Cost of Burnout in Todays Workforce|How to Train Your Brain for Long-Term Happiness|Why Gratitude is a Superpower Youre Not Using|What I Learned After 365 Days Without Social Media|The Psychology of First Impressions And How to Master Them|How to Build a Side Hustle That Pays Your Rent|5 Habits That Make You Instantly Likeable|Why Learning to Say No is a Game Changer|The Power of Walking Health Benefits Beyond Exercise|How to Read More Books Even If You Hate Reading|The One Rule Billionaires Follow Every Day|The Dark Side of Hustle Culture|What Makes a Great Leader Backed by Science|How to Build Trust in Any Relationship|What Happens When You Wake Up at 5AM for 30 Days|The Myth of Work-Life Balance And What to Do Instead|Why You Should Write Every Day Even if Youre Not a Writer|How Journaling Can Improve Your Mental Health|Why Motivation is Overrated and What Actually Works|The Art of Listening A Skill That Will Change Your Life|How to Break Bad Habits Without Willpower|The Secret to Getting Better Sleep Tonight|Why Creativity Isnt Just for Artists|The Rise of Quiet Quitting And What It Means for You|How Nature Improves Your Brain and Body|The Surprising Link Between Clutter and Anxiety|What I Learned From Talking to Strangers for a Week|The Psychology of Color How It Affects Your Mood|How to Handle Criticism Like a Pro|Why Curiosity is the Key to Innovation|How to Build Resilience in Tough Times|Why Most People Never Reach Their Full Potential|The Science of Happiness What Actually Works|How to Stop Comparing Yourself to Others|The Productivity Hacks Youre Not Using Yet|Why Introverts Make Great Leaders|The Power of Microhabits|How to Use Visualization to Achieve Your Goals|The Hidden Benefits of Boredom|How to Create a Life You Dont Need a Vacation From|Why You Should Rethink Your Definition of Success|The Unexpected Benefits of Doing Nothing|How to Stop Overthinking Everything|Why Small Talk Isnt So Small After All|The Secrets of Highly Persuasive People|How to Make Better Decisions Using Psychology|Why Failure is Essential for Growth|The Truth About Motivation Its Not What You Think|The Confidence Formula No One Talks About|What Great Thinkers Have in Common|How to Stop Letting Fear Control Your Life|Why Being Bored is Good for You|The Power of Asking Better Questions|Why Your Environment Shapes Your Habits|How to Find Your Passion When You Feel Lost|The Science of Willpower and Self-Control|Why You Should Learn to Be Alone|How to Build a Bulletproof Morning Routine|The Benefits of Saying I Dont Know|How to Master the Art of Self-Discipline|Why Feedback is Your Greatest Asset|The Most Overlooked Skill in Communication|What Happens When You Meditate Every Day for a Month|The Art of Making Difficult Conversations Easier|Why Simplicity is the New Productivity|How to Become a Lifelong Learner|Why Self-Awareness is a Leadership Superpower|The Future of Work What You Need to Know|How to Stay Motivated Without Burning Out|The Unexpected Power of Kindness|Why You Should Practice Mindful Eating|How to Master Focus in the Age of Distraction|The Secret to Long-Term Success Its Not Luck|What I Learned From Failing 10 Times in a Row|Why Learning Slower Might Make You Smarter|How to Deal with Uncertainty and Thrive|The Truth About Overnight Success Stories|Why Routine is More Powerful Than Inspiration|How to Build Stronger Social Connections|What Science Says About Happiness at Work|Why Time Management is Really Attention Management|How to Think More Clearly Under Pressure|What I Learned From 30 Days of Cold Showers|The Real Reason Youre Not Achieving Your Goals|Why Most People Stop Learning After School|The Science Behind Confidence and How to Build It|How to Turn Setbacks Into Stepping Stones|The Hidden Influence of Daily Rituals|Why Slowing Down Might Speed Up Your Success"
        parts = (content).split(" ")

    build = [parts[random.randint(1,len(parts)-1)]]
    #print(parts)
    for x in range(1,length):
        sample = []
        for y in range(1,len(parts)-2):
            if build[len(build)-1] == parts[y]:
                sample.append(parts[y+1])
        #print(sample)
        try:
            build.append(sample[random.randint(1,len(sample)-1)])
        except:
            try:
                build.append(sample[0])
            except:
                build.append(parts[random.randint(1,len(parts)-1)])
    return " ".join(build)

def generate(select):
    if select == 1:
        return "".join([f"{artical(select,random.randint(100,200))}| " for x in range(1,5)])
    else:
        return artical(select,random.randint(20,30))

#print(generate(2))
