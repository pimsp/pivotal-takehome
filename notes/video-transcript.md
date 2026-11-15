# Transcript: GT - AI in the human loop: GenAI in security service delivery

Adds: the transcript of the video watched earlier in the application (https://www.youtube.com/watch?v=K5hELUspWq8). Source: YouTube auto-generated English captions, fetched with yt-dlp on 2026-11-15; unedited, so names and terms may be mis-transcribed.

um hey everybody I'm uh pry I'll be talking about AI in the human Loop today so this is who I am I'll keep it brief 
I've been working at the intersection of AI and secop specifically um mostly focusing on analyst augmentation or 
Automation in security operations and outside of work I love you know talking about board games psychology human 
factors and today I'll be talking about a recent research project of mine and feel free to connect with me on LinkedIn 
I don't use X or Twitter that often so LinkedIn is the best way U so quick show of hands I know everybody's happy hour 
but I'd still like to know my audience uh how many of you here work in uh seops DNR okay and how many of you here 
consider yourselves to be like data scientists machine learning Engineers statisticians okay wonderful and how many of 
you here have done llm appd going beyond the basic chatbot prompting oh good good number of folks excellent I'd love to 
hear your thoughts and feedback um about how you've been measuring the productivity of some of the um llm apps that 
you've been using so the goal for today or my research project is how do llm based applications perform in a sock that 
handles millions of alerts across customers and I'm using the word llm specifically and not generative AI because I 
wanted to focus specifically on the large language models not necessarily the generative AI applications which can 
include a bunch of other things so before I started my research project one of the first things that I wanted to do was 
figure out what is the lay of the land right um what's in front of me and some of my awesome colleagues have done 
really interesting work um the team at SOS has done um good work in terms of benchmarking the security capabilities of 
large language models uh they've evaluated a bunch like converting Tech to SQL summarizations and their takeaway was 
most models only had about 50% accuracy like if you look at that graph there it's about like 50% accuracy and they've 
benchmarked a bunch of different um llms and the drawback at least according to me was that a lot of this was not 
implemented or measured with an analyst workflow and then at that point those were the best metrics available of course 
this field is exploding and everyday new metrics and measurements come about and this is um some of the results from um 
Microsoft's random control uh randomized control trial of security for uh of co-pilot for security and their takeaways 
were professionals were um less accurate in doing some report-based task and incident respon tasks incident response 
tasks and professionals were also slower in some some of the aspects but as novices or people who are newer to the 
industry and newer to the sock um were able to perform some of these tasks in a much better way the thing that they did 
at least for my understanding of their research paper is um they had two specific incidents that they conducted that 
they provided as part of the randomized control trial and all of the incidents were very um Defender native so I wanted 
to go a little beyond that push the envelope uh because this is great research and I wanted to take that one step 
further and what I did was this challenge accepted let's try to put large language models directly in an analyst 
workflow and let's also use alerts or incidents and investigations across different data sources different tooling not 
just limited to a couple of tools and this also had to happen within the uh existing SLA constraints that most security 
analysts operate under just a quick overview the first task here um as part of my research project is like how do we 
generate key findings a lot of people call this as incident report writing and um in our case we're doing this like on 
average we have about like 200 to 300 incidents and then there are like red team incidents we provide constant updates 
so is there anything here that we can use um llms for and one of the reasons we chose this it it is a complex task but 
one of the reasons we chose this was because there is a lot of natural language involved in it which is the strength of 
the llm um and not necessarily for doing a lot of pure reasoning based tasks which also comes under the LM systems but 
they're more like reinforcement learning based systems so this is one of our um tasks or use cases that we are testing 
out and then the next one is can we Orient an analyst who is dropped into a response environment with everything that 
is present in form of alerts and vendor data um is that something that we can do um the idea here was to kind of look 
at um the reasoning and find out if there are like outcomes that we can come up with that an analyst can Orient 
themselves all right so without beating uh beating around the bush too much um the first thing that I wanted to talk 
about is just this high level boxes right like this was the llm powered application the goal of this talk is to not 
tell you how to like develop an llm powered application but mostly to tell you about what factors to consider and how 
to design experiments to see if they truly provide the value and Roi that you need in your environment um so quickly 
here it is depending on you know the the kind of use case that we're using we provide a bunch of alerts enrichment 
along with it and then in some cases we'll have like potential remediation actions which is after and an investigation 
is conducted um and we documenti all of this send it to an llm model there are configurations such as prompt templates 
there are configurations like other hyper parameters like um the uh temperature values so those are all configurations 
and then finally we document the metrics offline and then the output comes around but where do we put the human in this 
one of the key aspects of our or one of the key goals of our experiment was to actually put this in in the um in the 
hands of our analyst and in an automated way without having them to like iterate on prompts continuously without having 
like a chat bot like situation because the novelty of a chat bot will fade very soon especially when you're in active 
response mode so data teams are always like show me the data we want more data and in my experience working at this 
intersection of security and um ml the security teams are almost like show me the results and then I can tell you 
whether things are good or not so it's always a tricky balance we want to introduce as minimum friction as possible 
while collecting meaningful data um so this was the key part of um of our uh research like trying to figure out how to 
uh best set up some of these experiments I think some of the talks earlier this this morning especially around the 
large scale fishing attack kind of um alluded to experiment design uh it only presented the results but I can go deeper 
into the experiment design so human in the loop is a common term where we talk about a collaborative approach where the 
humans are um where the humans are teaching machine learning models and training but wouldn't like the real outcome we 
we want is we want AI in the loop where AI is producing outputs and the humans are at the center of decision making so 
instead of doing a human in the loop we really want AI in the loop and this is one of the key aspects here we want the 
AI system to kind of produce outputs from the get-go right so the first approach for either of our experiments was we 
wanted to measure time um what does it look like you know when a single analyst is given a workflow with and without 
llms so that was our first approach but if you really think about it there is bias introduced here because the same 
analyst will be looking at the same incident and then there's a lot of duplicative effort this is definitely not 
acceptable the second approach is can we give a few analysts um like no llms and then another anal and a bunch of other 
analysts a few llms this is the classic um control versus test experiment setup however the question that came about 
here was what what if a few of these analysts are more experienced what if some of these analysts are not that 
experienced and will that affect the lift will that affect the outcome of our experiments so these were the challenges 
and in addition to that we wanted to provide a different combination of like models and get different types of feedback 
so if people have seen chatbot Arena that's exactly what chatbot Arena does um they have a bunch of uh different types 
of models but they don't tell you what actual model is until you type and get an answer so my question my prompt here 
was is hot dog a sandwich and then you can rate saying one was better the other one was not so good Tai we really 
thought about this does this really suffice in our condition probably not just getting thumbs up and thumbs down does 
not add a lot of meaningful information in terms of what we can leverage and confidently say yes this particular piece 
of information generated by the llm was good and something was not good so this did not really cut cut it for us um so 
we wanted to look at more automated ways of doing this and that's when we decid we set up an AB t uh AB test experiment 
bed so there are three different types of variants the first variant is obviously we want to run two different 
experiments the key findings generation and orienting an analyst as soon as they're dropped into this environment and 
the third variant is for every experiment we want to check how Junior analysts are performing how senior analysts are 
performing and finally for every group of analysts we also wanted to check um how different models are performing and 
um different parameters and configurations templates you know all the hyperparameters that go with us so this is the ab 
test um experiment setup um that that we Pro that we did um and finally the success of every experiment depends on the 
Integrity of how well the experiment is run one of the constraints or challenges that we had was that our analysts are 
very collaborative in nature so the senior and the junior analysts kind of work together which meant we cannot actually 
do an AB test but we had to come up with something called as like a Switchback test not necessarily come up it is 
fairly standard but a Switchback test is basically running the experiment um randomly it's still random but we switch 
back and forth across different time periods um so way even if there are network effects uh the impact of those effects 
are not very um persistent in the results of our experiments so this is our experiment design we did a Switchback test 
experiment and then finally this is like our llm generated output so yes the experimentation uh the ab test is 
producing results and now finally we wanted to measure um so what did we want to measure we wanted to measure things 
like time to edit the quality uh across both the use cases that we had and when it comes to measurements we're also 
doing automated measurements so here's an example where we provide some sort of um input which is what we provide uh as 
the input to the llm and then we have the llm generated output so an example here is in order to measure hallucination 
um the truth is is whatever we compute from the investigation and the claims is whatever we compute from the llm 
generated output so the if the truth like let's say we ask a question was a domain controller involved in this 
particular incident and if the truth says I don't know and if the claim was that yeah yes then that becomes a 
hallucination because the model is creating something that we're not very sure of it's an I don't know and 
contradiction is when it clearly violates um so the truth says the answer is no uh sorry the truth says the answer is 
yes and the claim says the answer is no so there a clear contradiction and then finally coverage is a key metric um 
let's say we asked the question was a webshell deployed and the truth says yes the claim also says yes that means the 
llm is picking out the right relevant context from whatever we're providing as the end input so this is um one such 
aspect and then this I mean the previous one is something that's fairly industry standard we call it question and 
answer generation and evaluation but this is um a different aspect which is what if we can identify signal gaps so 
let's say we have a reference document and the reference document is something where our analysts reflect on and 
provide their thoughts and they say we found a particular vulnerability and the analyst writes it up but it's not 
necessarily in our llm input at all and that is a critical Gap that we find in our data strategy so one of the Serendip 
outcomes of our experiments was to identify potential data gaps this is just an example that kind of walks you through 
that so the ones marked in green are things that were correctly identified this is the reference and the one on the 
right is the llm generator output it does create create a lot of hallucinations and incorrect uh data and then the one 
marked in the red box that is the one that the analyst or the human provided as an input and that is their reflection 
on the data uh which was something that the llm could not get because it was not present in the data in the first place 
and these help us really answer questions such as what is good um data strategy what is not so good should we focus on 
improving our modeling techniques prompting techniques or should we focus on improving things that are going in a 
signals so that is um a critical uh piece of outcome from our experiment and then in terms of results uh cost was uh 
something that definitely everybody considers uh cost was very easy for us to compute because uh initially everybody is 
like you know wanting to get people onto their platform so cost was definitely an easy Factor here to and cost of 
generating an incident was very low compared to the actual ones but the key results here are quality and time go hand 
inand better quality less edit times less time to write in case of palm and Germany you know the AI in the loop was 
beneficial the llm was able to write good things but in the case of a tuned model which was surprising the model 
learned some aspects and forgot all its inherent learned capabilities so in this case it was counterproductive and 
another thing that was which was surprising was initially we were concerned about alignment that is hallucinations um 
but hallucinations were not that much of a problem whereas coverage was a problem the model failed to retain a lot of 
the things that was actually provided in the form of input so I think these were the two things that we learned so far 
and sorry why would lose that happens sometimes during the tuning where when you're training some of the end layers of 
a large language model some of the inherent tasks it's just information POS POS is that what you were saying yes that 
could be one of the aspects here um I know I have to finish the talk so yeah yeah and finally this is our path forward 
we want to like do more analysis over different types of models threat types because this is not well covered or 
researched and uh we want to amplify the analy analyst provided signals so that's pretty much it these are the things 
that you need to ask as a data scientist you know do we need yes or no tasks I think that is a better takeaway instead 
of doing more complex tasks can we simply do intent classification and then as a security practitioner I think we 
should definitely ask questions as how much of an impact will this have on our workflow what will change what kind of 
feedback do I have to provide um I think these are things that we have to consider so that's it for me [Applause]
